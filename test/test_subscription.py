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
        subscription = SubscriptionFactory()
        self.assertEqual(subscription.next_payment_time(),
            datetime.strptime('2024-05-16 12:00:00', date_format) +
            timedelta(days=subscription.days_per_billing_cycle))
        subscription = SubscriptionFactory(start_date=datetime.strptime('2024-05-10 12:00:00', date_format).strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
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

if __name__ == '__main__':
    unittest.main()
