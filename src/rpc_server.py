import os
import threading
import subprocess
import platform
from src.rpc_config import RPCConfig

class RPCServer():
    def __init__(self, wallet):
        config = RPCConfig()
        self.wallet = wallet
        self.host = config.host
        self.port = config.port
        self.cli_path = config.cli_path
        self.rpc_is_ready = 0
        self.rpc_bind_port = config.bind_port
        self.process = None

    def _start(self):
        cmd = f'monero-wallet-rpc --wallet-file {self.wallet.name} --password ""'
        cmd += f' --rpc-bind-port {self.rpc_bind_port} --disable-rpc-login --confirm-external-bind'
        cmd += f' --daemon-host {self.host} --daemon-port {self.port}'

        if self.wallet.block_height:
            command = f'{self.cli_path} --wallet-file {os.path.join(self.wallet.path, self.wallet.name)}'
            command += f' --password "" --restore-height {self.wallet.block_height} --command exit'
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            blocks_synced = False

            while not blocks_synced:
                output = proc.stdout.readline().decode("utf-8").strip()

                print(f'SYNCING BLOCKS:{output}')

                if "Opened wallet:" in output:
                    blocks_synced = True
                    break

                if proc.poll() is not None:
                    break

        self.process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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
                print(f"Successfully killed monero-wallet-rpc with PID {pid}")
                self.rpc_is_ready = False
                break

            else:
                print("monero-wallet-rpc process not found")

    def start(self):
        self.kill()
        rpc_server_thread = threading.Thread(target=self._start())
        rpc_server_thread.start()
