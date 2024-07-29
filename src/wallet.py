import os
import platform
import logging
import logging.config
from config import node_url, wallet_dir
from src.clients.rpc import RPCClient
from src.logging import config as logging_config

class Wallet():
    def __init__(self, filename='subscriptions_wallet'):
        self.name = filename
        self.path = self._get_path()
        self._block_height = 0
        self._address = None
        self.status_message = "Starting"
        logging.config.dictConfig(logging_config)
        self.logger = logging.getLogger(self.__module__)

    def _get_path(self):
        path = ''
        if not platform.system() == 'Windows':
            path = os.getcwd()
        return path

    def get_current_block_height(self):
        # Send the JSON-RPC request to the daemon
        return RPCClient.get().current_block_height()

    def _daemon_address(self):
        node = node_url().split(':')
        return f'{node[0]}:{node[1]}'

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

    @property
    def address(self):
        if self._address is None:
            self._address = RPCClient.get().get_address()
        return self._address


    def exists(self):
        return os.path.isfile(f'{wallet_dir()}/{self.name}.keys') or os.path.isfile(f'{wallet_dir()}/{self.name}')

    def create(self):
        RPCClient.get().create_wallet()
