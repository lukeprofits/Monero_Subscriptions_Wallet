import os
import threading
import subprocess
import time
import logging
import logging.config
from src.rpc_config import RPCConfig
from src.environment import STAGENET
from src.rpc_client import RPCClient
from src.logging import config as logging_config
from src.interfaces.notifier import Notifier
from src.interfaces.observer import Observer
from src.wallet import Wallet

class RPCServer(Notifier):
    _wallet_servers = {}

    @classmethod
    def get(cls, wallet=Wallet()):
        if not cls._wallet_servers.get(wallet.name):
            cls._wallet_servers[wallet.name] = cls(wallet)
        return cls._wallet_servers[wallet.name]

    def __init__(self, wallet=Wallet()):
        self.config = RPCConfig()
        self.wallet = wallet
        self.host = self.config.host
        self.port = self.config.port
        self.wallet_cli_path = self.config.cli_path
        self.rpc_is_ready = 0
        self.rpc_bind_port = self.config.bind_port
        self.process = None
        self.wallet_process = None
        logging.config.dictConfig(logging_config)
        self.logger = logging.getLogger(self.__module__)
        self.failed_to_start = False
        self.status_message = ''
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def _start_wallet(self):
        command = f'{self.wallet_cli_path} --wallet-file {os.path.join(self.wallet.path, self.wallet.name)}'
        command += f' --password "" --restore-height {self.wallet.block_height} --daemon-address {self.host}:{self.port}'
        command += ' --command refresh'
        self.logger.debug(command)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.wallet_process = proc

    def _start_rpc(self):
        cmd = f'stdbuf -oL monero-wallet-rpc --wallet-file {self.wallet.name} --password ""'
        cmd += f' --rpc-bind-port {self.rpc_bind_port} --disable-rpc-login --confirm-external-bind'
        cmd += f' --daemon-address {self.host}:{self.port}'
        if STAGENET:
            cmd += ' --stagenet'

        self.logger.debug(cmd)

        self.process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def wallet_started(self):
        blocks_synced = False

        while not blocks_synced:
            stdout = self.wallet_process.stdout.readline()
            self.logger.debug(stdout)

            if "Refresh done" in stdout and "Error" not in stdout:
                blocks_synced = True
                break

            if "Error" in stdout:
                self.failed_to_start = True

            if self.wallet_process.poll() is not None:
                break

        return not self.failed_to_start

    def _start(self):
        self.logger.debug(f'Block Height: {self.wallet.block_height}')

        if self.wallet.block_height:
            self._start_wallet()
            self.wallet_started()

        self.logger.debug(f'{self.host}:{self.port}')
        self._start_rpc()

    def kill(self):
        self.logger.debug('Killing RPC Server Process')
        self.process.kill()
        self.logger.debug('Killing Wallet CLI Process')
        self.wallet_process.kill()

    def rpc_server_ready(self):
        rpc_client = RPCClient()
        while True:
            while not rpc_client.local_healthcheck() and not self.failed_to_start:
                output = self.process.stdout.readline()
                if self.process.poll() is not None:
                    break

                if output:
                    self.status_message = output.strip()
                    self.notify()

                time.sleep(0.1)

            if not self.wallet.exists():
                self.wallet.create()

            if not self.failed_to_start:
                self.status_message = "Ready"
                self.notify()

            if self.failed_to_start:
                self.status_message = 'Failed To Start RPC Server - Check Logs'
                self.notify()

            break


    def check_if_rpc_server_ready(self):
        self.logger.debug('Checking if RPC Ready')
        threading.Thread(target=self.rpc_server_ready).start()

    def start(self):
        self._start()