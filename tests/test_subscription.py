import unittest
import datetime
from tests.rpc_client import RPCClientMock
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

    def test_check_date_for_how_many_days_until_payment_needed(self):
        sub = Subscription(**self._full_test_attributes())
        days_away = 60
        self.assertEqual(sub.check_date_for_how_many_days_until_payment_needed(datetime.datetime.now() + datetime.timedelta(days=days_away)), days_away)

    def test_encode_decode(self):
        sub = Subscription(**self._full_test_attributes())
        encoded_sub = sub.encode()
        decoded_sub = Subscription(**Subscription.decode(encoded_sub))
        self.assertEqual(sub.json_friendly(), decoded_sub.json_friendly())

    def test_valid_check(self):
        sub = Subscription(**self._no_optional_attributes())
        self.assertEqual(sub.custom_label, '')
        self.assertEqual(sub.amount, 1.1)
        self.assertEqual(sub.billing_cycle_days, 30)
        self.assertEqual(sub.start_date, datetime.date.today())
        self.assertEqual(sub.sellers_wallet, '888tNkZrPN6JsEgekjMnABU4TBzc2Dt29EPAvkRxbANsAnjyPbb3iQ1YBRk1UXcdRsiKc9dhwMVgN5S9cQUiyoogDavup3H')
        self.assertEqual(sub.valid_check(), True)
        prev_amount = sub.amount
        sub.amount = None
        self.assertEqual(sub.valid_check(), False)
        sub.amount = prev_amount
        prev_currency = sub.currency
        sub.currency = ''
        self.assertEqual(sub.valid_check(), False)
        sub.currency = prev_currency
        prev_sellers_wallet = sub.sellers_wallet
        sub.sellers_wallet = ''
        self.assertEqual(sub.valid_check(), False)
        sub.sellers_wallet = prev_sellers_wallet
        prev_billing_cycle_days = sub.billing_cycle_days
        sub.billing_cycle_days = ''
        self.assertEqual(sub.valid_check(), False)
        sub.billing_cycle_days = prev_billing_cycle_days
        prev_start_date = sub.start_date
        sub.start_date = None
        self.assertEqual(sub.valid_check(), False)
        sub.start_date = prev_start_date
        self.assertEqual(sub.valid_check(), True)

    def test_loop_transactions(self):
        sub = Subscription(**self._full_test_attributes())
        sub.rpc_client = RPCClientMock()
        for payment_id, dest_address, transaction_date in sub.loop_transactions():
            self.assertEqual(payment_id, '1a2b3c4d5e6f7a8b')
            self.assertEqual(dest_address, '888tNkZrPN6JsEgekjMnABU4TBzc2Dt29EPAvkRxbANsAnjyPbb3iQ1YBRk1UXcdRsiKc9dhwMVgN5S9cQUiyoogDavup3H')
            self.assertEqual(transaction_date.date(), datetime.datetime.now().date())

    def test_determine_if_a_payment_is_due(self):
        sub = Subscription(**self._full_test_attributes())
        sub.rpc_client = RPCClientMock()
        self.assertEqual(sub.determine_if_a_payment_is_due(), True)
        sub = Subscription(**self._full_test_attributes())
        sub.rpc_client = RPCClientMock()
        sub.rpc_client.transfers([{
            'payment_id': '1a2b3c4d5e6f7a8b',
            'destinations': [
                {
                    'address': '888tNkZrPN6JsEgekjMnABU4TBzc2Dt29EPAvkRxbANsAnjyPbb3iQ1YBRk1UXcdRsiKc9dhwMVgN5S9cQUiyoogDavup3H'
                }
            ],
            'timestamp': datetime.datetime.timestamp(datetime.datetime.now() - datetime.timedelta(seconds=60))
        }])
        self.assertEqual(sub.determine_if_a_payment_is_due(), False)

    def test_renewal_date(self):
        sub = Subscription(**self._full_test_attributes())
        sub.rpc_client = RPCClientMock()
        self.assertEqual(sub.renewal_date(), datetime.date.today().strftime(Subscription.DATE_FORMAT))
        sub.rpc_client.transfers([{
            'payment_id': '1a2b3c4d5e6f7a8b',
            'destinations': [
                {
                    'address': '888tNkZrPN6JsEgekjMnABU4TBzc2Dt29EPAvkRxbANsAnjyPbb3iQ1YBRk1UXcdRsiKc9dhwMVgN5S9cQUiyoogDavup3H'
                }
            ],
            'timestamp': datetime.datetime.timestamp(datetime.datetime.now() - datetime.timedelta(seconds=60))
        }])
        self.assertEqual(sub.renewal_date(), (datetime.date.today() + datetime.timedelta(days=sub.billing_cycle_days)).strftime(Subscription.DATE_FORMAT))

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