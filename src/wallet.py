import os
import platform
import threading
import subprocess
import requests
import json

class Wallet():
    def __init__(self, daemon_rpc_url):
        self.name = "subscriptions_wallet"
        self.path = self._get_path()
        self._block_height = 0
        self._cli_path = None
        self.daemon_rpc_url = daemon_rpc_url

    @property
    def cli_path(self):
        if not self._cli_path:
            if platform.system() == 'Windows':
                cli_path = "" + 'monero-wallet-cli.exe'  # Update path to the location of the monero-wallet-cli executable if your on WINDOWS
            else:
                cli_path = 'monero-wallet-cli'  # Update path to the location of the monero-wallet-cli executable if your on other platforms
            self._cli_path = cli_path
        return self._cli_path

    def _get_path(self):
        path = ''
        if not platform.system() == 'Windows':
            path = os.getcwd()
        return path

    def get_current_block_height(self):
        # Set up the JSON-RPC request
        headers = {'content-type': 'application/json'}
        data = {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_info"
        }

        # Send the JSON-RPC request to the daemon
        response = requests.post(self.daemon_rpc_url, data=json.dumps(data), headers=headers)

        # Parse the response to get the block height
        if response.status_code == 200:
            response_data = response.json()
            block_height = response_data["result"]["height"]
            print(f'Block Height: {block_height}')
            return block_height

        else:
            return None

    @property
    def block_height(self):
        if not os.path.isfile(f"{self.name}.keys") or not os.path.isfile(self.name):
            # If either file doesn't exist
            self._block_height = self.get_current_block_height()
            self.create()
        else:
            # If both files exist, do nothing
            print('Wallet exists already.')
        return self._block_height

    def create(self):
        # Remove existing wallet if present
        try:
            os.remove(self.name)
        except:
            pass

        try:
            os.remove(f'{self.name}.keys')
        except:
            pass

        command = f"{self.cli_path} --generate-new-wallet {os.path.join(self.path, self.name)} --mnemonic-language English --command exit"
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Sending two newline characters, pressing 'Enter' twice
        process.stdin.write('\n')
        process.stdin.write('\n')
        process.stdin.flush()

        # Getting the output and error messages
        stdout, stderr = process.communicate()
        #print(stdout)
        #print(stderr)

        worked_check = process.returncode
        if worked_check == 0:
            output_text = stdout
            wallet_address = output_text.split('Generated new wallet: ')[1].split('View key: ')[0].strip()
            view_key = output_text.split('View key: ')[1].split('*********************')[0].strip()
            seed = output_text.split(' of your immediate control.')[1].split('********')[0].strip().replace('\n', '')
            print(f'wallet_address: {wallet_address}')
            print(f'view_key: {view_key}')
            print(f'seed: {seed}')

            with open(file=f'{self.name}_seed.txt', mode='a', encoding='utf-8') as f:
                f.write(f'Wallet Address:\n{wallet_address}\nView Key:\n{view_key}\nSeed:\n{seed}\n\nThe above wallet should not be your main source of funds. This is ONLY to be a side account for paying monthly subscriptions. If anyone gets access to this seed, they can steal all your funds. Please use responsibly.\n\n\n\n')

            return seed, wallet_address, view_key
        else:
            print(stderr)