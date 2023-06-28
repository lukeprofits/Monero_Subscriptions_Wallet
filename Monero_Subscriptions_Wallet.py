import threading
from multiprocessing import Process, Pipe
from lxml import html
from src.subscriptions import Subscriptions, Subscription
from src.ui.node_picker import NodePicker
from src.wallet import Wallet
from src.rpc_server import RPCServer
from src.ui.please_wait import PleaseWait
from src.ui.subscription import SubscriptionUI
from src.thread_manager import ThreadManager
from src.ui.banner import Banner
# from src.ui.wallet import Wallet
from src.ui.balance import Balance
from src.ui.subscriptions import SubscriptionsUI
from src.ui.deposit import Deposit
from src.ui.withdrawl import Withdrawl
from src.ui.subscription_ui import SubscriptionUI
import kivy
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
kivy.require('2.2.1')
import json
from kivy.app import App
from kivy.uix.label import Label
import time
import requests
import random
from src.rpc_config import RPCConfig
from src.rpc_client import RPCClient
from src.ui.node_picker import NodePicker

# please_wait = PleaseWait()
# please_wait.open()

# while not rpc_server.rpc_is_ready:
#     # Check for window events
#     event, values = please_wait.update()  # Read with a timeout so the window is updated

# print('\n\nRPC Server has started')

# wallet_balance_xmr = '--.------------'
# wallet_balance_usd = '---.--'
# wallet_address = wallet.address()

# try:
#     wallet_balance_xmr, wallet_balance_usd, xmr_unlocked_balance = wallet.balance()
# except:
#     pass

# # Start a thread to send the payments
# threading.Thread(target=subscriptions.send_recurring_payments).start()

# please_wait.close()

class DefaultWindow(Screen):
    pass

class SubscriptionTypeWindow(Screen):
    pass

class ManualSubscriptionWindow(Screen):
    def add_subscription(self):
        sub_attrs = {}

        for field, sub_attr in self.ids.items():
            sub_attrs[field] = sub_attr.text

        subscription = Subscription(**sub_attrs)

        if subscription.valid_check():
            subscriptions = Subscriptions()
            subscriptions.add_subscription(subscription)
            subscriptions.write_subscriptions()
            self.parent.current = 'default'
            sub_ui = None
            for widget in self.walk():
                if type(widget) == SubscriptionsUI:
                    sub_ui = widget
                    break
            sub_ui.reload_data()
        else:
            for field, sub_attr in self.ids.items():
                if not getattr(subscription, f'{field}_valid'):
                    #Doesn't actually work to notify users, but on the right track.
                    sub_attr.background_color = [0,0,1,1]

class MerchantSubscriptionWindow(Screen):
    def add_subscription(self):
        try:
            subscription = Subscription(**Subscription.decode(self.ids.subscription_code.text))
            if subscription.valid_check():
                subscriptions = Subscriptions()
                subscriptions.add_subscription(subscription)
                subscriptions.write_subscriptions()
                self.parent.current = 'default'
            else:
                self.ids.subscription_code
        except json.decoder.JSONDecodeError:
            self.ids.subscription_code
            #Communicate invalidity to user

class Loading(Screen):
    pass

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('default_window.kv')

class WalletApp(App):
    def on_start(self):
        self.wallet = Wallet()
        self.rpc_server = RPCServer(self.wallet)
        kv.current = 'loading'
        print('Scheduling RPC Start')
        rpc_server = threading.Thread(target=Clock.schedule_once, args=[self.start_rpc_server])
        rpc_server.run()
        print('Scheduled RPC Start')
        print('Scheduling RPC Start Check')
        rpc_server_check = threading.Thread(target=self.check_if_rpc_server_ready)
        rpc_server_check.start()
        print('Scheduled RPC Start Check')

    def set_default(self, dt):
        kv.current = 'default'

    def on_stop(self):
        self.rpc_server.kill

    def build(self):
        return kv

    def start_rpc_server(self, dt):
        self.rpc_server.start()

    def check_if_rpc_server_ready(self):
        rpc_client = RPCClient()
        while not rpc_client.local_healthcheck():
            time.sleep(1)
            print('Checking if RPC Ready')
        Clock.schedule_once(self.set_default)

        if not self.wallet.exists():
            self.wallet.create()

        self.wallet.generate_qr()
        return False

if __name__ == '__main__':
    # Get subscriptions list
    # subscriptions = Subscriptions()

    # # # ADD DAEMON/NODE ######################################################################################################
    # node_picker = NodePicker()

    # if not node_picker.node_picked():
    #     node_picker.pick_node()
    #     node_picker.close_window()

    # # # START PREREQUISITES ##################################################################################################
    # threading.Thread(target=subscription_gui.update_balance).start()
    # threading.Thread(target=subscriptions.send_recurring_payments).start()

    # wallet = Wallet()
    # rpc_server = RPCServer(wallet)

    wallet_app = WalletApp()

    # wallet_app.rpc_server = rpc_server
    # wallet_app.wallet = wallet

    # wallet_app.start_rpc_server()

    # rpc_server_check = threading.Thread(target=Clock.schedule_interval, args=[wallet_app.check_if_rpc_server_ready, 1])
    # rpc_server_check.run()

    WalletApp().run()

# subscription_gui = SubscriptionUI()
# window = subscription_gui.main_window()
# threading.Thread(target=subscription_gui.update_balance).start()
# subscription_gui.event_loop()
# ThreadManager.stop_flag().set()
# window.close()