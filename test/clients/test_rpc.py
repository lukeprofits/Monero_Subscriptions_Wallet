import unittest
from src.clients.rpc import RPCClient
from test.utils.rpc_server_helper import rpc_server_test

class testRPCClient(unittest.TestCase):
    def test_current_block_height(self):
        return None
        # for _ in rpc_server_test():
        # client = RPCClient()
        # self.assertEqual(client.get_version(), 65563)

if __name__ == '__main__':
    unittest.main()