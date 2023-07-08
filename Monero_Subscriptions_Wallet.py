import threading
from src.wallet import Wallet
from src.rpc_server import RPCServer
from src.rpc_config import RPCConfig
import kivy
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
import time
from src.rpc_client import RPCClient
import pystray
from src.subscriptions import Subscriptions
from src.thread_manager import ThreadManager
from src.ui.system_tray_icon import SystemTrayIcon
from src.ui.node_picker import NodePicker
from src.ui.balance import Balance
from src.ui.subscriptions import SubscriptionsUI
from src.ui.subscription import SubscriptionUI
from src.ui.deposit import Deposit
from src.ui.withdrawl import Withdrawl
from src.ui.manual_subscription_form import ManualSubscriptionForm
from src.ui.merchant_subscription_window import MerchantSubscriptionWindow
from src.ui.loading import Loading
from src.utils import walk_for_widget
from kivy.config import Config
from kivy.uix.image import Image
import logging

kivy.require('2.2.1')

class DefaultWindow(Screen):
    def on_pre_enter(self):
        image = walk_for_widget(self, Image)
        image.reload()

class SubscriptionTypeWindow(Screen):
    pass

class ManualSubscriptionWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class WalletApp(App):
    def on_start(self):
        self.title = 'Monero Subscription Wallet'
        self.wallet = Wallet()
        self.rpc_server = RPCServer(self.wallet)
        self.subscriptions = Subscriptions()
        self.rpc_config = RPCConfig()
        self.icon = 'icon.png'
        self.set_node_picker()
        if self.rpc_config.host:
            self.set_loading()
            subscriptions_payment = threading.Thread(target=self.pay_subscriptions)
            subscriptions_payment.start()

    def set_default(self, _ = None):
        self.wm.current = 'default'

    def set_node_picker(self, _ = None):
        self.wm.current = 'node_picker'

    def set_loading(self, _ = None):
        self.wm.current = 'loading'

    def on_stop(self):
        self.rpc_server.kill()
        self._icon.stop()
        ThreadManager.stop_flag().set()

    def build(self):
        self.wm = Builder.load_file('default_window.kv')
        return self.wm

    def start_rpc_server(self, dt):
        self.rpc_server.start()

    def pay_subscriptions(self):
        self.subscriptions.set_subscriptions(self.subscriptions.read_subscriptions())
        self.subscriptions.send_recurring_payments()

    def show_window(self, dt):
        print('Showing Window')
        self.wm.parent.show()

    def restore_to_front(self):
        print('Restoring To Front')
        Clock.schedule_once(self.show_window)

    def hide_window(self, dt):
        print('Hiding Window')
        self.wm.parent.hide()

    def to_taskbar(self):
        print('Restoring To Front')
        Clock.schedule_once(self.hide_window)

if __name__ == '__main__':
    wallet_app = WalletApp()

    icon = SystemTrayIcon(wallet_app.to_taskbar, wallet_app.restore_to_front)

    wallet_app._icon = icon

    threading.Thread(target=icon.thread_run).start()
    wallet_app.run()
