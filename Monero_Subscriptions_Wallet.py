import threading
from src.wallet import Wallet
from src.rpc_server import RPCServer
import kivy
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
import time
from src.rpc_client import RPCClient
import pystray
from PIL import Image, ImageDraw
kivy.require('2.2.1')

class DefaultWindow(Screen):
    pass

class SubscriptionTypeWindow(Screen):
    pass

class ManualSubscriptionWindow(Screen):
    pass

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

    def show_window(self, dt):
        print('Showing Window')
        kv.parent.show()

    def restore_to_front(self):
        print('Restoring To Front')
        Clock.schedule_once(self.show_window)

    def hide_window(self, dt):
        print('Hiding Window')
        kv.parent.hide()

    def to_taskbar(self):
        print('Restoring To Front')
        Clock.schedule_once(self.hide_window)


def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2),
        fill=color2)
    dc.rectangle(
        (0, height // 2, width // 2, height),
        fill=color2)

    return image

if __name__ == '__main__':

    # threading.Thread(target=subscriptions.send_recurring_payments).start()

    wallet_app = WalletApp()

    icon = pystray.Icon('Monero Subscription Wallet',\
        icon=create_image(64,64, 'black', 'white'),\
        menu=pystray.Menu(
            pystray.MenuItem('Hide', wallet_app.to_taskbar),
            pystray.MenuItem('Show', wallet_app.restore_to_front)
        )
    )

    threading.Thread(target=icon.run).start()
    wallet_app.run()
