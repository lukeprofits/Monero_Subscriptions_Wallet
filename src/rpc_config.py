class RPCConfig():
    NODE_FILENAME = 'node_to_use.txt'

    def __init__(self):
        self._node = self.node()
        self.host = self._node.split(':')[0]
        self.port = self._node.split(':')[1]
        self.bind_port = '18088'
        self.local_url = f'http://127.0.0.1:{self.bind_port}/json_rpc'
        self.username = 'monero'
        self.password = 'monero'
        self.daemon_url = f'http://{self.host}:{self.port}/json_rpc'

    def node(self):
        with open(self.NODE_FILENAME, 'r') as f:
            node = f.readline().strip()  # read first line into 'node'
        return node