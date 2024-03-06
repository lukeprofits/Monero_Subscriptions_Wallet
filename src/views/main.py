import customtkinter as ctk
from src.interfaces.view import View
from src.rpc_server import RPCServer
from src.observers.rpc_server_status_observer import RPCServerStatusObserver

class MainView(View):
    def __init__(self, app):
        self._app = app
        self._rpc_server = RPCServer.get()
        self._element_observers = []

    def build(self):
        # Sync Status
        sync_status = self.add(ctk.CTkLabel(self._app, text='( Sync Status )'))
        observer = RPCServerStatusObserver(sync_status)  # TODO: Make this get the status and display it in sync status
        self._element_observers.append(observer)
        self._rpc_server.attach(observer)
        sync_status.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Settings Button
        settings_button = self.add(ctk.CTkButton(self._app, text="⚙", font=("Helvetica", 24), width=35, height=30, command=self.open_settings))
        settings_button.grid(row=0, column=2, padx=20, pady=10, sticky="e")

        # Amount
        amount = self.add(ctk.CTkLabel(self._app, text="$150.00 USD", font=("Helvetica", 48)))
        amount.grid(row=1, column=0, columnspan=3, padx=10, pady=0, sticky="nsew")

        # Frame to hold buttons
        center_frame = self.add(ctk.CTkFrame(self._app, ))
        center_frame.grid(row=3, column=0, columnspan=3, padx=0, pady=10, sticky="nsew")
        center_frame.columnconfigure([0, 1], weight=1)  # Frame will span 3 columns but contain two columns (0 and 1)

        # Receive Button
        self.receive_button = ctk.CTkButton(center_frame, text="Receive", command=self.open_recieve)
        self.receive_button.grid(row=0, column=0, padx=(10, 5), pady=(0, 10), sticky="ew")

        # Pay Button
        self.pay_button = ctk.CTkButton(center_frame, text="Pay", command=self.open_pay)
        self.pay_button.grid(row=0, column=1, padx=(5, 10), pady=(0, 10), sticky="ew")

        # Manage Subscriptions Button
        self.subscriptions_button = ctk.CTkButton(center_frame, text="Manage Subscriptions", command=self.open_subscriptions)
        self.subscriptions_button.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="ew")

        return self



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