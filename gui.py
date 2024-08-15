from tkinter import PhotoImage

import customtkinter as ctk
from src.rpc_server import RPCServer
from config import rpc, is_first_launch
from src.views import (MainView, ReceiveView, PayView, SubscriptionsView, SettingsView, SetCurrencyView,
                       NodeSelectionView, AmountView, ReviewRequestView, ReviewSendView, ReviewDeleteRequestView,
                       WelcomeView, CreatePaymentRequestView, CopyPaymentRequestView)
import config as cfg
from src.exchange import Exchange

ctk.set_default_color_theme("monero_theme.json")

# TODO: Get this from the config file first. If not present, use what is currently set below.

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.define_all_views()
        self.spawn_appropriate_initial_window()
        self.start_rpc_server_if_appropriate()

    def define_all_views(self):
        self.views = {
            'main': MainView(self),
            'recieve': ReceiveView(self),
            'pay': PayView(self),
            'subscriptions': SubscriptionsView(self),
            'settings': SettingsView(self),
            'set_currency': SetCurrencyView(self),
            'node_selection': NodeSelectionView(self),
            'amount': AmountView(self),
            'review_request': ReviewRequestView(self),
            'review_send': ReviewSendView(self),
            'review_delete': ReviewDeleteRequestView(self),
            'welcome': WelcomeView(self),
            'create_payment_request': CreatePaymentRequestView(self),
            'copy_payment_request': CopyPaymentRequestView(self)
        }

    def spawn_appropriate_initial_window(self):
        if is_first_launch() == 'True':
            self.current_view = self.views['welcome'].build()
        else:
            self.current_view = self.views['main'].build()

    def start_rpc_server_if_appropriate(self):
        if rpc() == 'True':
            self.rpc_server = RPCServer.get()
            self.rpc_server.start()
            self.rpc_server.check_readiness()

    def switch_view(self, view_name: str):
        self.current_view.destroy()
        self.current_view = self.views[view_name]
        self.current_view.build()

    def shutdown_steps(self):
        self.destroy()
        if rpc() == 'True':
            self.rpc_server.kill()


app = App()
app.title("Monero Subscriptions Wallet")
app.iconphoto(True, PhotoImage(file='icon_orange.png'))
app.protocol("WM_DELETE_WINDOW", app.shutdown_steps)
app.resizable(False, False)  # Make the window non-resizable
app.mainloop()
