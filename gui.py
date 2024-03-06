import random

import customtkinter as ctk

import subscription_functions
import config as cfg

from src.rpc_server import RPCServer
from src.views.main import MainView
from src.views.recieve import RecieveView
from src.views.pay import PayView
from src.views.subscriptions import SubscriptionsView
from src.views.settings import SettingsView

ctk.set_default_color_theme("monero_theme.json")

# VARIABLES TO MOVE TO CONFIG
CURRENCY_OPTIONS = ["USD", "XMR", "BTC", "EUR", "GBP"]  # Is there a library for pulling these in automatically?'

# TODO: Get this from the config file first. If not present, use what is currently set below.
DEFAULT_CURRENCY = CURRENCY_OPTIONS[0]
SECONDARY_CURRENCY = CURRENCY_OPTIONS[1]


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x195")
        # 3 columns 2 rows

        # Configure the main window grid for spacing and alignment
        self.columnconfigure([0, 1, 2], weight=1)

        # Define what the views are
        self.views = {
            'main': MainView(self),
            'recieve': RecieveView(self),
            'pay': PayView(self),
            'subscriptions': SubscriptionsView(self),
            'settings': SettingsView(self)
        }

        self.current_view = self.views['main'].build()
        self.rpc_server = RPCServer.get()

    def switch_view(self, view_name: str):
        self.current_view.destroy()
        view = self.views[view_name]
        self.current_view = view.build()

    def shutdown_steps(self):
        self.destroy()
        self.rpc_server.kill()


app = App()
app.protocol("WM_DELETE_WINDOW", app.shutdown_steps)
app.mainloop()