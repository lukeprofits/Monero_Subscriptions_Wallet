import customtkinter as ctk
from src.interfaces.view import View
from src.rpc_server import RPCServer
from src.observers.rpc_server_status_observer import RPCServerStatusObserver

class MainView(View):
    CURRENCY_OPTIONS = ["USD", "XMR", "BTC", "EUR", "GBP"]

    def __init__(self, app):
        self._app = app
        self._rpc_server = RPCServer.get()
        self._element_observers = []

    def build(self):
        self.sync_status()
        self.settings_button()
        self.amount()
        self.selected_currency()
        self.center_frame()
        return self

    def sync_status(self):
        sync_status = self.add(ctk.CTkLabel(self._app, text='( Sync Status )'))
        observer = RPCServerStatusObserver(sync_status)
        self._element_observers.append(observer)
        self._rpc_server.attach(observer)
        sync_status.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        return sync_status

    def settings_button(self):
        settings_button = self.add(ctk.CTkButton(self._app, text="⚙", font=("Helvetica", 24), width=35, height=30, command=self.open_settings))
        settings_button.grid(row=0, column=2, padx=20, pady=10, sticky="e")
        return settings_button

    def amount(self):
        amount = self.add(ctk.CTkLabel(self._app, text="$150.00 USD", font=("Helvetica", 48)))
        amount.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        return amount

    def selected_currency(self):
        selected_currency = ctk.StringVar(value=self.CURRENCY_OPTIONS[0])
        currency_selector = self.add(ctk.CTkOptionMenu(self._app, width=25, values=self.CURRENCY_OPTIONS, command=self.currency_selector_callback, variable=selected_currency))
        currency_selector.grid(row=2, column=1)
        return currency_selector

    def center_frame(self):
        center_frame = self.add(ctk.CTkFrame(self._app,))
        center_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        center_frame.columnconfigure([0, 1, 2], weight=1)
        self.receive_button(center_frame)
        self.pay_button(center_frame)
        self.subscriptions_button(center_frame)
        return center_frame

    def receive_button(self, master):
        receive_button = ctk.CTkButton(master, text="Receive", command=self.open_recieve)
        receive_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        return receive_button

    def pay_button(self, master):
        pay_button = ctk.CTkButton(master, text="Pay", command=self.open_pay)
        pay_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
        return pay_button

    def subscriptions_button(self, master):
        subscriptions_button = ctk.CTkButton(master, text="Manage Subscriptions", command=self.open_subscriptions)
        subscriptions_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        return subscriptions_button

    def open_subscriptions(self):
        self._app.switch_view('subscriptions')

    def open_recieve(self):
        self._app.switch_view('recieve')

    def open_pay(self):
        self._app.switch_view('pay')

    def open_settings(self):
        self._app.switch_view('settings')

    def currency_selector_callback(self, choice):
        SELECTED_CURRENCY = choice
        print("User chose:", choice)
        print(SELECTED_CURRENCY)

    def destroy(self):
        super().destroy()
        for observer in self._element_observers:
            self._rpc_server.detach(observer)
        self._element_observers = []