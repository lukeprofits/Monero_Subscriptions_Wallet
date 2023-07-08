import unittest
from src.subscriptions import Subscriptions
from tests.factories.subscription import SubscriptionFactory
class SubscriptionsTest(unittest.TestCase):
    def setUp(self):
        Subscriptions.SUBS_FILE_PATH = 'tests/fixtures/Subscriptions.json'
        self.subscriptions = Subscriptions()
        self.sub = SubscriptionFactory()
    def test_read_subscriptions(self):
        self.assertEqual(self.subscriptions._subscriptions, [])

    def test_write_subscriptions(self):
        self.subscriptions.add_subscription(self.sub)
        self.subscriptions.write_subscriptions()
        subs = self.subscriptions.read_subscriptions()
        for sub in subs:
            self.assertEqual(sub.json_friendly(), self.sub.json_friendly())

    def test_find_index(self):
        self.subscriptions.add_subscription(self.sub)
        second_sub = SubscriptionFactory()
        second_sub.custom_label = 'Test 2'
        self.subscriptions.add_subscription(second_sub)
        index = self.subscriptions.find_index(self.sub.custom_label, self.sub.amount, self.sub.billing_cycle_days)
        self.assertEqual(index, 0)
        index = self.subscriptions.find_index(second_sub.custom_label, second_sub.amount, second_sub.billing_cycle_days)
        self.assertEqual(index, 1)

    def test_find_subscription(self):
        self.subscriptions.add_subscription(self.sub)
        second_sub = SubscriptionFactory()
        second_sub.custom_label = 'Test 2'
        self.subscriptions.add_subscription(second_sub)
        matched_sub = self.subscriptions.find_subscription(self.sub.custom_label, self.sub.amount, self.sub.billing_cycle_days)
        self.assertEqual(matched_sub, self.sub)
        matched_sub = self.subscriptions.find_subscription(second_sub.custom_label, second_sub.amount, second_sub.billing_cycle_days)
        self.assertEqual(matched_sub, second_sub)

    def tearDown(self):
        self.subscriptions.set_subscriptions([])
        self.subscriptions.write_subscriptions()