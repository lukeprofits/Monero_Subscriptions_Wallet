from src.subscription import Subscription

class SubscriptionFactory(Subscription):
    def __init__(self):
        super().__init__(**self._full_test_attributes())

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