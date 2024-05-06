import customtkinter as ctk
from src.rpc_server import RPCServer
from src.views import (MainView, ReceiveView, PayView, SubscriptionsView, SettingsView, SetCurrencyView,
                       NodeSelectionView, AmountView, ReviewRequestView, ReviewSendView, ReviewDeleteRequestView,
                       WelcomeView)
import config as cfg
from src.exchange import Exchange

ctk.set_default_color_theme("monero_theme.json")

# TODO: Get this from the config file first. If not present, use what is currently set below.

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if cfg.rpc:
            self.rpc_server = RPCServer.get()
            self.rpc_server.start()
            self.rpc_server.check_readiness()
            Exchange.refresh_prices()

        # Define what the views are
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
            'welcome': WelcomeView(self)
        }

        self.current_view = self.views['main'].build()

    def switch_view(self, view_name: str):
        self.current_view.destroy()
        self.current_view = self.views[view_name]
        self.current_view.build()

    def shutdown_steps(self):
        self.destroy()
        self.rpc_server.kill()

app = App()
app.title("Monero Subscriptions Wallet")
app.protocol("WM_DELETE_WINDOW", app.shutdown_steps)
app.mainloop()