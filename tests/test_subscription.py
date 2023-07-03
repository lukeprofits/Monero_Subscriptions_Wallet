import unittest
import datetime
from src.subscription import Subscription

class SubscriptionTest(unittest.TestCase):
    def test_full_creation(self):
        sub = Subscription(**self._full_test_attributes())
        self.assertEqual(sub.custom_label, 'Test')
        self.assertEqual(sub.amount, 1.1)
        self.assertEqual(sub.billing_cycle_days, 30)
        self.assertEqual(sub.start_date, datetime.date(2023, 1, 1))
        self.assertEqual(sub.sellers_wallet, '888tNkZrPN6JsEgekjMnABU4TBzc2Dt29EPAvkRxbANsAnjyPbb3iQ1YBRk1UXcdRsiKc9dhwMVgN5S9cQUiyoogDavup3H')
        self.assertEqual(sub.currency, 'XMR')
        self.assertEqual(sub.payment_id, '1a2b3c4d5e6f7a8b')

    def test_optional_creation(self):
        sub = Subscription(**self._no_optional_attributes())
        self.assertEqual(sub.custom_label, '')
        self.assertEqual(sub.amount, 1.1)
        self.assertEqual(sub.billing_cycle_days, 30)
        self.assertEqual(sub.start_date, datetime.date.today())
        self.assertEqual(sub.sellers_wallet, '888tNkZrPN6JsEgekjMnABU4TBzc2Dt29EPAvkRxbANsAnjyPbb3iQ1YBRk1UXcdRsiKc9dhwMVgN5S9cQUiyoogDavup3H')

    def test_json_friendly(self):
        sub = Subscription(**self._full_test_attributes())
        json_attributes = sub.json_friendly()
        self.assertEqual(json_attributes['custom_label'], 'Test')
        self.assertEqual(json_attributes['amount'], 1.1)
        self.assertEqual(json_attributes['billing_cycle_days'], 30)
        self.assertEqual(json_attributes['start_date'], '2023-01-01')
        self.assertEqual(json_attributes['sellers_wallet'], '888tNkZrPN6JsEgekjMnABU4TBzc2Dt29EPAvkRxbANsAnjyPbb3iQ1YBRk1UXcdRsiKc9dhwMVgN5S9cQUiyoogDavup3H')
        self.assertEqual(json_attributes['currency'], 'XMR')
        self.assertEqual(json_attributes['payment_id'], '1a2b3c4d5e6f7a8b')

    def test_currency_validity(self):
        sub = Subscription(**self._full_test_attributes())
        self.assertEqual(sub.amount_valid(), True)
        sub.amount = ''
        self.assertEqual(sub.amount_valid(), False)

    def test_payment_id_validity(self):
        sub = Subscription(**self._full_test_attributes())
        self.assertEqual(sub.payment_id_valid(), True)
        sub.payment_id = '1a2b3c4d5e6f7g8h'
        self.assertEqual(sub.payment_id_valid(), False)

    def test_start_date_validity(self):
        sub = Subscription(**self._full_test_attributes())
        self.assertEqual(sub.start_date_valid(), True)
        sub.start_date = '2023-01-01'
        self.assertEqual(sub.start_date_valid(), False)

    def test_billing_cycle_days_validity(self):
        sub = Subscription(**self._full_test_attributes())
        self.assertEqual(sub.billing_cycle_days_valid(), True)
        sub.billing_cycle_days = '1'
        self.assertEqual(sub.billing_cycle_days_valid(), False)

    def test_sellers_wallet_validity(self):
        sub = Subscription(**self._full_test_attributes())
        self.assertEqual(sub.sellers_wallet_valid(), True)
        sub.sellers_wallet = '12345'
        self.assertEqual(sub.sellers_wallet_valid(), False)

    def _full_test_attributes(self):
        return {
            'custom_label': 'Test',
            'amount': '1.1',
            'billing_cycle_days': '30',
            'start_date': '2023-01-01',
            'sellers_wallet': '888tNkZrPN6JsEgekjMnABU4TBzc2Dt29EPAvkRxbANsAnjyPbb3iQ1YBRk1UXcdRsiKc9dhwMVgN5S9cQUiyoogDavup3H',
            'currency': 'XMR',
            'payment_id': '1a2b3c4d5e6f7a8b'
        }

    def _no_optional_attributes(self):
        full_attributes = self._full_test_attributes()
        full_attributes.pop('start_date')
        full_attributes.pop('payment_id')
        full_attributes.pop('custom_label')
        return full_attributes