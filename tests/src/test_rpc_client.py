import unittest
from src.rpc_server import RPCServer
from src.rpc_client import RPCClient
from src.wallet import Wallet

class testRPCClient(unittest.TestCase):
    def setUp(self):
        super().setUp()
        wallet = Wallet('test_wallet')
        self.rpc_server = RPCServer(wallet)
        self.rpc_server.start()
        self.rpc_server.rpc_server_ready()

    def tearDown(self):
        super().tearDown()
        self.rpc_server.kill()

    def test_current_block_height(self):
        client = RPCClient()
        self.assertEqual(client.get_version(), 65562)

if __name__ == '__main__':
    unittest.main()