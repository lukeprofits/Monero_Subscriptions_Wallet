import os
import platform
import subprocess
import logging
import logging.config
from src.rpc_config import RPCConfig
from src.rpc_client import RPCClient
from src.logging import config as logging_config

class Wallet():
    def __init__(self, filename='subscriptions_wallet'):
        self.name = filename
        self.path = self._get_path()
        self._block_height = 0
        self._address = None
        self.config = RPCConfig()
        logging.config.dictConfig(logging_config)
        self.logger = logging.getLogger(self.__module__)

    def _get_path(self):
        path = ''
        if not platform.system() == 'Windows':
            path = os.getcwd()
        return path

    def get_current_block_height(self):
        # Send the JSON-RPC request to the daemon
        return RPCClient().current_block_height()

    @property
    def block_height(self):
        if not self._block_height:
            if not self.exists():
                # If either file doesn't exist
                self.create()
            else:
                # If both files exist, do nothing
                self.logger.info('Wallet exists already.')

            self._block_height = self.get_current_block_height()
        return self._block_height

    def exists(self):
        return os.path.isfile(f"{self.name}.keys") or os.path.isfile(self.name)

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

        command = f"{self.config.cli_path} --generate-new-wallet {os.path.join(self.path, self.name)} --mnemonic-language English --command exit"
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Sending two newline characters, pressing 'Enter' twice
        process.stdin.write('\n')
        process.stdin.write('\n')
        process.stdin.flush()

        # Getting the output and error messages
        stdout, stderr = process.communicate()

        worked_check = process.returncode
        if worked_check == 0:
            output_text = stdout
            wallet_address = output_text.split('Generated new wallet: ')[1].split('View key: ')[0].strip()
            view_key = output_text.split('View key: ')[1].split('*********************')[0].strip()
            seed = output_text.split(' of your immediate control.')[1].split('********')[0].strip().replace('\n', '')
            self.logger.info(f'wallet_address: {wallet_address}')
            self.logger.info(f'view_key: {view_key}')
            self.logger.info(f'seed: {seed}')

            with open(file=f'{self.name}_seed.txt', mode='a', encoding='utf-8') as f:
                f.write(f'Wallet Address:\n{wallet_address}\nView Key:\n{view_key}\nSeed:\n{seed}\n\nThe above wallet should not be your main source of funds. This is ONLY to be a side account for paying monthly subscriptions. If anyone gets access to this seed, they can steal all your funds. Please use responsibly.\n\n\n\n')

            return seed, wallet_address, view_key
        else:
            self.logger.info(stderr)