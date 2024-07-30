import threading
import subprocess
import time
import logging
import logging.config
from config import node_url, rpc_bind_port, wallet_dir, rpc
from src.environment import STAGENET
from src.clients.rpc import RPCClient
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
        self.wallet = wallet
        self.rpc_is_ready = 0
        self.process = None
        self.wallet_process = None
        logging.config.dictConfig(logging_config)
        self.logger = logging.getLogger(self.__module__)
        self.failed_to_start = False
        self.successful_start = False
        self.status_message = ''
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def _daemon_address(self):
        node = node_url().split(':')
        return f'{node[0]}:{node[1]}'

    def _start_rpc(self):
        cmd = f'stdbuf -oL monero-wallet-rpc --password "" --wallet-dir {wallet_dir()}'
        cmd += f' --rpc-bind-port {rpc_bind_port()} --disable-rpc-login --confirm-external-bind'
        cmd += f' --daemon-address {self._daemon_address()}'
        if STAGENET:
            cmd += ' --stagenet'

        self.logger.debug(cmd)

        self.process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def kill(self):
        self.logger.debug('Killing RPC Server Process')
        self.process.kill()

    def ready(self):
        rpc_client = RPCClient.get()
        while True:
            while not rpc_client.local_healthcheck() and not self.failed_to_start:
                output = self.process.stdout.readline()
                self.logger.debug(output.strip())
                status = self.process.poll()
                self.logger.debug(f'Poll: {status}')
                if status is not None:
                    if status != 0 or "Initial refresh failed" in output:
                        self.failed_to_start = True
                    break

                if 'THROW EXCEPTION' in output or 'needs to connect to a monero deamon' in output:
                    self.failed_to_start = True
                    break

                if output:
                    self.status_message = f'RPC Server: {output.strip()}'
                    self.notify()

                time.sleep(0.1)

            if not self.wallet.exists():
                self.wallet.create()

            if not self.failed_to_start:
                self.status_message = 'RPC Server: Ready'
                rpc_client.open_wallet()
                self.logger.debug(rpc_client.refresh())
                self.notify()

            if self.failed_to_start:
                self.status_message = 'RPC Server: Failed To Start'
                self.notify()

            if not rpc() == 'True':
                self.status_message = "( Test Mode )"
                self.notify()

            break

    def check_readiness(self):
        self.logger.debug('Checking if RPC Ready')
        threading.Thread(target=self.ready).start()

    def start(self):
        self._start_rpc()
