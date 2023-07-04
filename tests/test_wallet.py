import os
import unittest
from tests.rpc_client import RPCClientMock
from src.wallet import Wallet

class WalletTest(unittest.TestCase):
    def setUp(self):
        self.wallet = Wallet()
        self.wallet.rpc_client = RPCClientMock()
        self.wallet.rpc_client.fetch_address({'address': '45JjUxWGBmzbA9H8St5cD2PGV2JuvpvXzY4rv6pCrTWSTY5hRwaAjSJi9ZxWxhoDmRiHnPmmoQ8RmZAVMukNGEsEPNSPT2B'})
        self.wallet.median_usd_price = 150.0

    def test_calculate_usd_exchange(self):
        self.assertEqual(self.wallet.calculate_usd_exchange(1), 150)

    def test_balance(self):
        self.assertEqual(self.wallet.balance(), (2.0, '300.00', 2.0))

    def test_amount_available(self):
        self.assertEqual(self.wallet.amount_available(2, 'XMR'), True)
        self.assertEqual(self.wallet.amount_available(2.1, 'XMR'), False)
        self.assertEqual(self.wallet.amount_available(150.0, 'USD'), True)
        self.assertEqual(self.wallet.amount_available(301.0, 'USD'), False)

    def test_address(self):
        self.assertEqual(self.wallet.address(), '45JjUxWGBmzbA9H8St5cD2PGV2JuvpvXzY4rv6pCrTWSTY5hRwaAjSJi9ZxWxhoDmRiHnPmmoQ8RmZAVMukNGEsEPNSPT2B')

    def test_get_current_block_height(self):
        self.assertEqual(self.wallet.get_current_block_height(), 0)

    def test_generate_qr(self):
        if os.path.isfile('wallet_qr_code.png'):
            os.remove('wallet_qr_code.png')
        self.wallet.generate_qr()
        self.assertEqual(os.path.isfile('wallet_qr_code.png'), True)
        os.remove('wallet_qr_code.png')