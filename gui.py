import customtkinter as ctk
from src.rpc_server import RPCServer
from src.views import MainView, ReceiveView, PayView, SubscriptionsView, SettingsView, SetCurrencyView, NodeSelectionView
import config as cfg

ctk.set_default_color_theme("monero_theme.json")

# TODO: Get this from the config file first. If not present, use what is currently set below.
DEFAULT_CURRENCY = cfg.CURRENCY_OPTIONS[0]
SECONDARY_CURRENCY = cfg.CURRENCY_OPTIONS[1]

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define what the views are
        self.views = {
            'main': MainView(self),
            'recieve': ReceiveView(self),
            'pay': PayView(self),
            'subscriptions': SubscriptionsView(self),
            'settings': SettingsView(self),
            'set_currency': SetCurrencyView(self),
            'node_selection': NodeSelectionView(self)
        }

        self.current_view = self.views['main'].build()
        if cfg.rpc:
            self.rpc_server = RPCServer.get()
            self.rpc_server.start()
            self.rpc_server.check_readiness()

    def switch_view(self, view_name: str):
        self.current_view.destroy()
        self.current_view = self.views[view_name]
        self.current_view.build()

    def shutdown_steps(self):
        self.destroy()
        self.rpc_server.kill()

app = App()
app.protocol("WM_DELETE_WINDOW", app.shutdown_steps)
app.mainloop()