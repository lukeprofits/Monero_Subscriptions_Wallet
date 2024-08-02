import unittest
import vcr
from src.clients.rpc import RPCClient

class testRPCClient(unittest.TestCase):
    def test_version(self):
        with vcr.use_cassette('test/fixtures/cassettes/version.yaml'):
            client = RPCClient()
            version = client.get_version()
        self.assertEqual(version, 65563)

    def test_get_address(self):
        with vcr.use_cassette('test/fixtures/cassettes/address.yaml'):
            client = RPCClient()
            address = client.get_address()
        self.assertEqual(address, '59fhPNhFLEx3zP16ZAPaeHXsPoNczVaGo245CgDSW9WpiMxvP1N7WdxX1RA4vob6ABGGBxUgjcCN2LjeSGPiH8AEKpAMFKC')

    def test_get_balance(self):
        with vcr.use_cassette('test/fixtures/cassettes/get_balance.yaml'):
            client = RPCClient()
            balance = client.get_balance()
        self.assertEqual(balance, 52561416412713)

    def test_make_integrated_address(self):
        with vcr.use_cassette('test/fixtures/cassettes/integrated_address.yaml'):
            client = RPCClient()
            address = '59fhPNhFLEx3zP16ZAPaeHXsPoNczVaGo245CgDSW9WpiMxvP1N7WdxX1RA4vob6ABGGBxUgjcCN2LjeSGPiH8AEKpAMFKC'
            payment_id = '075eed614ebea072'
            integrated_address = client.make_integrated_address(address, payment_id)
        self.assertEqual(integrated_address['integrated_address'], '5KNNQBWjwWU3zP16ZAPaeHXsPoNczVaGo245CgDSW9WpiMxvP1N7WdxX1RA4vob6ABGGBxUgjcCN2LjeSGPiH8AEUmgrwoxBZLKDt8PcKB')

    def test_transfer(self):
        with vcr.use_cassette('test/fixtures/cassettes/transfer.yaml'):
            client = RPCClient()
            address = '59fhPNhFLEx3zP16ZAPaeHXsPoNczVaGo245CgDSW9WpiMxvP1N7WdxX1RA4vob6ABGGBxUgjcCN2LjeSGPiH8AEKpAMFKC'
            result = client.transfer(address, 1000)
        self.assertEqual(result['amount'], 1000)

    def test_create_wallet(self):
        with vcr.use_cassette('test/fixtures/cassettes/create_wallet.yaml'):
            client = RPCClient()
            result = client.create_wallet('test_wallet_2')
        self.assertEqual(result, {})

    def test_open_wallet(self):
        with vcr.use_cassette('test/fixtures/cassettes/open_wallet.yaml'):
            client = RPCClient()
            result = client.open_wallet('test_wallet_2')
        self.assertEqual(result, {})

'''
To create a new test with the wallet rpc server started use
for _ in rpc_server_test():
    with vcr.use_cassette(filename):

The rpc_server_test line can be removed once the cassette is created.
'''
if __name__ == '__main__':
    unittest.main()