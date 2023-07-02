from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, NumericProperty
from src.subscriptions import Subscriptions
class SubscriptionUI(RecycleDataViewBehavior, GridLayout):
    amount = NumericProperty(0)
    custom_label = StringProperty('')
    renewal_date = StringProperty('')
    billing_cycle_days = NumericProperty(0)

    def __init__(self, **kwargs):
        super(SubscriptionUI, self).__init__(**kwargs)

    def remove_subscription(self, custom_label, amount, billing_cycle_days):
        subs = Subscriptions()
        sub = subs.find_subscription(custom_label, amount, billing_cycle_days)
        if sub:
            subs.remove_subscription(sub)
            subs.write_subscriptions()
            self.parent.parent.reload_data()