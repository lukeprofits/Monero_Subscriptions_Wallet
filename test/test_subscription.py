import unittest
import time_machine
from unittest.mock import patch
from datetime import datetime, timedelta
from src.subscription import Subscription
from test.factories.subscription import SubscriptionFactory

class TestSubscription(unittest.TestCase):
    @time_machine.travel('2024-05-16 12:00:00')
    def test_next_payment_time(self):
        date_format = '%Y-%m-%d %H:%M:%S'
        subscription = SubscriptionFactory(start_date=datetime.strptime('2024-05-9 12:00:00', date_format).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')
        self.assertEqual(subscription.next_payment_time(),
            datetime.strptime('2024-05-16 12:00:00', date_format) +
            timedelta(days=subscription.days_per_billing_cycle))
        subscription = SubscriptionFactory(start_date=datetime.strptime('2024-05-10 12:00:00', date_format).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')
        self.assertEqual(subscription.next_payment_time(), datetime.strptime('2024-05-17 12:00:00', date_format))

    def test_json_friendly(self):
        subscription = SubscriptionFactory()
        self.assertEqual(subscription.json_friendly(), {
            'custom_label': subscription.custom_label,
            'sellers_wallet': subscription.sellers_wallet,
            'currency': subscription.currency,
            'amount': subscription.amount,
            'payment_id': subscription.payment_id,
            'start_date': subscription.start_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z',
            'days_per_billing_cycle': subscription.days_per_billing_cycle,
            'number_of_payments': subscription.number_of_payments,
            'change_indicator_url': subscription.change_indicator_url
        })

    def test_encode(self):
        subscription = SubscriptionFactory(
            custom_label='test_label',
            sellers_wallet='4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S',
            currency='USD',
            amount='10',
            payment_id='abcdef1234567890',
            start_date=datetime.strptime('2024-05-10 12:00:00', '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            days_per_billing_cycle=7,
            number_of_payments=10,
            change_indicator_url=''
        )
        self.assertEqual(subscription.encode(), 'monero-request:1:H4sIAAAAAAACAy2OW0/DMAyF/0ueO5R2vbC+taNFAoHENsbYS5SLexFpMiUp0CL+OymaZMk+/qzj84PooEflUI5CjALEO6paIL0SPadOGzIa6dlCRmNA8cmr1/3d/8I6PRBJGSwnDqy7igAJOllyAUNYL2WvWsInLgHlWYDUODAPdEMudBpAOYvyEAfoqkgvvBllXEATRus4SbPbzZLMgpRgLPmivi9548KtT4n5PE6Xg27aYYTnjd28ODOLHSTlCLWxH8W5D7NSv7NunqyeZ/1Ul+n8pg6P4n6bFt9Vwaoq4XO9W3d+emB2iLstnKL98tJR44igzidHEY7iFU5WIT6EUY6xrxuM8Rn9/gFqTg5MRAEAAA==')

    def test_decode(self):
        subscription = SubscriptionFactory()
        sub_copy = Subscription(**Subscription.decode(subscription.encode()))
        self.assertEqual(subscription.custom_label, sub_copy.custom_label)
        self.assertEqual(subscription.sellers_wallet, sub_copy.sellers_wallet)
        self.assertEqual(subscription.currency, sub_copy.currency)
        self.assertEqual(subscription.amount, sub_copy.amount)
        self.assertEqual(subscription.payment_id, sub_copy.payment_id)
        self.assertEqual(subscription.start_date, sub_copy.start_date)
        self.assertEqual(subscription.days_per_billing_cycle, sub_copy.days_per_billing_cycle)
        self.assertEqual(subscription.number_of_payments, sub_copy.number_of_payments)
        self.assertEqual(subscription.change_indicator_url, sub_copy.change_indicator_url)

if __name__ == '__main__':
    unittest.main()
