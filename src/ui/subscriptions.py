from src.subscriptions import Subscriptions
from kivy.uix.recycleview import RecycleView

class SubscriptionsUI(RecycleView):
    def __init__(self, **kwargs):
        super(SubscriptionsUI, self).__init__(**kwargs)
        self.subscriptions = Subscriptions()
        self.data = self.load_subscriptions_data()

    def load_subscriptions_data(self):
        return [
            {
                'amount': str(sub.amount),
                'custom_label': sub.custom_label,
                'renewal_date': sub.renewal_date(),
                'billing_cycle_days': sub.billing_cycle_days
            } for sub in self.subscriptions.read_subscriptions()
        ]

    def reload_data(self):
        self.data = self.load_subscriptions_data()