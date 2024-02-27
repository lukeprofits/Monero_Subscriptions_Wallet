import platform
import os
import random
from src.environment import STAGENET

class RPCConfig():
    NODE_FILENAME = 'node_to_use.txt'

    def __init__(self):
        self._node = self.node()
        self.host = self._node.split(':')[0] if self._node else ''
        self.port = self._node.split(':')[1] if self._node else ''
        self.bind_port = '18088'
        self.local_url = f'http://127.0.0.1:{self.bind_port}/json_rpc'
        self.username = 'monero'
        self.password = 'monero'
        self._daemon_url = f'http://{self.host}:{self.port}/json_rpc'
        self._cli_path = None

    def node(self):
        node = None
        if os.path.isfile(self.NODE_FILENAME):
            with open(self.NODE_FILENAME, 'r') as f:
                node = f.readline().strip()  # read first line into 'node'
        else:
            with open(self.NODE_FILENAME, 'w') as f:
                f.write(self.random_node())
        return node

    def set_node(self, node):
        with open(self.NODE_FILENAME, 'w') as f:
            f.write(node)

    @property
    def cli_path(self):
        if not self._cli_path:
            if platform.system() == 'Windows':
                cli_path = "" + 'monero-wallet-cli.exe'
            else:
                cli_path = 'monero-wallet-cli'
            self._cli_path = cli_path
        return self._cli_path

    @property
    def daemon_url(self):
        if STAGENET:
            self._daemon_url = 'https://testnet.xmr.ditatompel.com/json_rpc'
        return self._daemon_url

    def random_node(self):
        return random.choice([
            'xmr-node.cakewallet.com:18081'
        ])