from kivy.uix.gridlayout  import GridLayout
from src.utils import walk_for_widget
from src.subscriptions import Subscriptions
from src.subscription import Subscription
from src.ui.common import CommonTheme
from src.ui.manual_subscription_form_inputs import ManualSubscriptionFormInputs
from src.ui.subscriptions import SubscriptionsUI

class ManualSubscriptionForm(GridLayout):
    def add_subscription(self):
        sub_attrs = {}
        inputs = walk_for_widget(self, ManualSubscriptionFormInputs)
        for field, sub_attr in inputs.ids.items():
            sub_attrs[field] = sub_attr.text

        subscription = Subscription(**sub_attrs)

        if subscription.valid_check():
            subscriptions = Subscriptions()
            subscriptions.add_subscription(subscription)
            subscriptions.write_subscriptions()
            self.parent.parent.parent.current = 'default'
            sub_ui = walk_for_widget(self, SubscriptionsUI)
            sub_ui.reload_data()
            for field, sub_attr in inputs.ids.items():
                sub_attr.text = ''
        else:
            for field, sub_attr in inputs.ids.items():
                if not getattr(subscription, f'{field}_valid')():
                    sub_attr.background_color = CommonTheme().monero_orange
