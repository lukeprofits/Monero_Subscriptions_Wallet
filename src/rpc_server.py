import os
import threading
import subprocess
import platform
import time
import logging
import logging.config
from src.rpc_config import RPCConfig
from src.environment import STAGENET
from src.rpc_client import RPCClient
from src.logging import config as logging_config

class RPCServer():
    def __init__(self, wallet):
        self.config = RPCConfig()
        self.wallet = wallet
        self.host = self.config.host
        self.port = self.config.port
        self.cli_path = self.config.cli_path
        self.rpc_is_ready = 0
        self.rpc_bind_port = self.config.bind_port
        self.process = None
        logging.config.dictConfig(logging_config)
        self.logger = logging.getLogger(self.__module__)
        self.failed_to_start = False

    def _start(self, label):
        self.logger.debug(f'Block Height: {self.wallet.block_height}')

        if self.wallet.block_height:
            command = f'{self.cli_path} --wallet-file {os.path.join(self.wallet.path, self.wallet.name)}'
            command += f' --password "" --restore-height {self.wallet.block_height} --command refresh'
            self.logger.debug(command)
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            stdout, stderr = proc.communicate()

            blocks_synced = False

            while not blocks_synced:
                self.logger.debug(f'SYNCING BLOCKS:{stdout}')
                self.logger.error(("Opened wallet:" in stdout))

                if "Opened wallet:" in stdout and "Error" not in stdout:
                    blocks_synced = True
                    break

                if "Error" in stdout:
                    label.configure(text=stderr)
                    self.failed_to_start = True

                if proc.poll() is not None:
                    break

        cmd = f'stdbuf -oL monero-wallet-rpc --wallet-file {self.wallet.name} --password ""'
        cmd += f' --rpc-bind-port {self.rpc_bind_port} --disable-rpc-login --confirm-external-bind'
        cmd += f' --daemon-host {self.host} --daemon-port {self.port}'
        if STAGENET:
            cmd += ' --stagenet'

        self.logger.debug(cmd)

        self.process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def kill(self):
        # Check which platform we are on and get the process list accordingly
        if platform.system() == 'Windows':
            process = subprocess.Popen("tasklist", stdout=subprocess.PIPE)
            rpc_path = 'monero-wallet-rpc.exe'
        else:
            process = subprocess.Popen("ps", stdout=subprocess.PIPE)
            rpc_path = 'monero-wallet-r'
        out, err = process.communicate()

        for line in out.splitlines():
            if rpc_path.encode() in line:
                if platform.system() == 'Windows': # Check if we are on Windows and get the PID accordingly
                    pid = int(line.split()[1].decode("utf-8"))
                else:
                    pid = int(line.split()[0].decode("utf-8"))
                os.kill(pid, 9)
                self.logger.debug(f"Successfully killed monero-wallet-rpc with PID {pid}")
                self.rpc_is_ready = False
                break

            else:
                self.logger.info("monero-wallet-rpc process not found")

    def rpc_server_ready(self, label):
        rpc_client = RPCClient()
        while True:
            while not rpc_client.local_healthcheck() and not self.failed_to_start:
                self.logger.debug(self.failed_to_start)
                self.logger.debug('Running HealthCheck...')
                output = self.process.stdout.readline()
                if self.process.poll() is not None:
                    break
                if output:
                    label.configure(text=output.strip())
                time.sleep(1)

            if not self.wallet.exists():
                self.wallet.create()

            if not self.failed_to_start:
                label.configure(text="Ready")

            if self.failed_to_start:
                label.configure(text='Failed To Start RPC Server - Check Logs')

            break


    def check_if_rpc_server_ready(self, rpc_status_label):
        self.logger.debug('Checking if RPC Ready')
        threading.Thread(target=self.rpc_server_ready, args=[rpc_status_label]).start()

    def start(self, label):
        self.kill()
        self._start(label)