import json
from src.subscriptions import Subscriptions
from src.subscription import Subscription
from src.utils import walk_for_widget
from kivy.uix.screenmanager import Screen
from src.ui.common import CommonTheme
from src.ui.subscriptions import SubscriptionsUI

class MerchantSubscriptionWindow(Screen):
    def add_subscription(self):
        try:
            subscription = Subscription(**Subscription.decode(self.ids.subscription_code.text))
            if subscription.valid_check():
                subscriptions = Subscriptions()
                subscriptions.add_subscription(subscription)
                subscriptions.write_subscriptions()
                self.parent.current = 'default'
                sub_ui = walk_for_widget(self, SubscriptionsUI)
                sub_ui.reload_data()
            else:
                self.ids.subscription_code
        except (json.decoder.JSONDecodeError, Exception):
            self.ids.subscription_code.background_color = CommonTheme().monero_orange
            #Communicate invalidity to user
