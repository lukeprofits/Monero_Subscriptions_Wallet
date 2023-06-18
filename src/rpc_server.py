import os
import threading
import subprocess
import platform

class RPCServer():
    def __init__(self, wallet, config):
        self.wallet = wallet
        self.host = config.host
        self.port = config.port
        self.rpc_is_ready = 0
        self.rpc_bind_port = config.bind_port
        self._cli_path = None

    def cli_path(self):
        if not self._cli_path:
            if platform.system() == 'Windows':
                cli_path = "" + 'monero-wallet-cli.exe'  # Update path to the location of the monero-wallet-cli executable if your on WINDOWS
            else:
                cli_path = 'monero-wallet-cli'  # Update path to the location of the monero-wallet-cli executable if your on other platforms
            self._cli_path = cli_path
        return self._cli_path

    def _start(self):
        cmd = f'monero-wallet-rpc --wallet-file {self.wallet.name} --password "" --rpc-bind-port {self.rpc_bind_port} --disable-rpc-login --confirm-external-bind --daemon-host {self.host} --daemon-port {self.port}'

        if self.wallet.block_height:
            command = f'{self.cli_path} --wallet-file {os.path.join(self.wallet.path, self.wallet.name)} --password "" --restore-height {self.wallet.block_height} --command exit'
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

        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while True:
            output = process.stdout.readline().decode("utf-8").strip()
            print(f'RPC STARTING:{output}')

            if "Starting wallet RPC server" in output:
                self.rpc_is_ready = True
                break

            if process.poll() is not None:
                break

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
