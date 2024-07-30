import unittest
from src.clients.rpc import RPCClient
from test.utils.rpc_server_helper import rpc_server_test

class testRPCClient(unittest.TestCase):
    def test_current_block_height(self):
        for _ in rpc_server_test():
            client = RPCClient()
            version = client.get_version()
        self.assertEqual(version, 65563)


if __name__ == '__main__':
    unittest.main()