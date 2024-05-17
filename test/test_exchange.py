import unittest
from unittest.mock import patch
from src.exchange import Exchange

class TestExchange(unittest.TestCase):
    def test_convert(self):
        with patch('src.exchange.xe_scrape', return_value=2):
            Exchange.USD_AMOUNT = 12345
            self.assertEqual(Exchange.convert('BTC'), '24,690.00000000')

        with patch('src.exchange.goldback_scrape', return_value=2):
            Exchange.USD_AMOUNT = 10000
            self.assertEqual(Exchange.convert('XGB'), '20,000.00')

        Exchange.XMR_AMOUNT = 2

        self.assertEqual(Exchange.convert('XMR'), '2.00')

    def test_to_xmr(self):
        Exchange.USD_AMOUNT = 150
        Exchange.XMR_AMOUNT = 1
        Exchange.US_EXCHANGE = 150
        with patch('src.exchange.xe_scrape', return_value='.8'):
            self.assertEqual(Exchange.to_atomic_units('GBP', 5), 26666666666)

    def test_display(self):
        with patch('src.exchange.Exchange.convert', return_value='10,000.00'):
            self.assertEqual(Exchange.display('USD'), '$10,000.00 USD')

if __name__ == '__main__':
    unittest.main()
