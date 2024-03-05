import customtkinter as ctk
from src.rpc_server import RPCServer
from src.views.main import MainView
from src.views.recieve import RecieveView
from src.views.pay import PayView
from src.views.subscriptions import SubscriptionsView
from src.views.settings import SettingsView

ctk.set_default_color_theme("monero_theme.json")

# VARIABLES TO MOVE TO CONFIG
CURRENCY_OPTIONS = ["USD", "XMR", "BTC", "EUR", "GBP"]  # Is there a library for pulling these in automatically?
SELECTED_CURRENCY = CURRENCY_OPTIONS[0]

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x260")
        # 3 columns 2 rows

        # Configure the main window grid for spacing and alignment
        self.columnconfigure([0, 1, 2], weight=1)

        self.views = {
            'main': MainView(self),
            'recieve': RecieveView(self),
            'pay': PayView(self),
            'subscriptions': SubscriptionsView(self),
            'settings': SettingsView(self)
        }

        self.current_view = self.views['main'].build()
        self.rpc_server = RPCServer.get()
        self.rpc_server.start()
        self.rpc_server.check_if_rpc_server_ready()

        # Selector Button
        #self.receive_button = ctk.CTkButton(center_frame, text="XMR", width=10, command=self.open_recieve)
        #self.receive_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.toplevel_window = None

    def switch_view(self, view_name: str):
        self.current_view.destroy()
        view = self.views[view_name]
        self.current_view = view.build()

    def shutdown_steps(self):
        self.rpc_server.kill()
        self.destroy()

class NodeSelection(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="Node Selection")
        self.label.pack(padx=20, pady=20)


        self.toplevel_window = None

class WelcomeMessage(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="Welcome Message")
        self.label.pack(padx=20, pady=20)


class AddPaymentRequest(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="Add Payment Request")
        self.label.pack(padx=20, pady=20)


class ManuallyCreatePaymentRequest(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="Manually Create Payment Request")
        self.label.pack(padx=20, pady=20)


app = App()
app.protocol("WM_DELETE_WINDOW", app.shutdown_steps)
app.mainloop()