import customtkinter as ctk
from src.interfaces.view import View
from src.rpc_server import RPCServer
from src.observers.status_label_observer import StatusLabelObserver
import config as cfg
import styles
from config import default_currency, secondary_currency
from src.wallet import Wallet
from src.exchange import Exchange

class MainView(View):
    def __init__(self, app):
        super().__init__(app)
        self._wallet = Wallet()
        self._rpc_server = RPCServer.get(self._wallet)
        self._element_observers = []
        self.toplevel_window = None

    def build(self):
        self._app.geometry(styles.MAIN_VIEW_GEOMETRY)

        # Configure the main window grid for spacing and alignment
        self._app.columnconfigure([0, 1, 2], weight=1)  # 3 columns 2 rows

        # Sync Status
        rpc_status = self.add(ctk.CTkLabel(self._app, text=f'RPC Status: {self._rpc_server.status_message or "( Sync Status )"}'))
        rpc_observer = StatusLabelObserver(rpc_status)
        self._element_observers.append(rpc_observer)
        self._rpc_server.attach(rpc_observer)

        rpc_status.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Settings Button
        settings_button = self.add(ctk.CTkButton(self._app, text=styles.SETTINGS_BUTTON_EMOJI, font=(styles.font, 24), width=35, height=30, command=self.open_settings))
        settings_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # Amount
        self.amount = self.add(ctk.CTkLabel(self._app, text=self._get_currency_text(), font=(styles.font, 48)))
        self.amount.grid(row=1, column=0, columnspan=3, padx=10, pady=0, sticky="nsew")

        # Bind the click event
        self.amount.bind("<Button-1>", self._toggle_currency)

        # Frame to hold buttons
        center_frame = self.add(ctk.CTkFrame(self._app, ))
        center_frame.grid(row=3, column=0, columnspan=3, padx=0, pady=10, sticky="nsew")
        center_frame.columnconfigure([0, 1], weight=1)  # Frame will span 3 columns but contain two columns (0 and 1)

        # Receive Button
        receive_button = ctk.CTkButton(center_frame, text="Receive", corner_radius=15, command=self.open_recieve)
        receive_button.grid(row=0, column=0, padx=(10, 5), pady=(0, 10), sticky="ew")

        # Pay Button
        pay_button = ctk.CTkButton(center_frame, text="Pay", corner_radius=15, command=self.open_pay)
        pay_button.grid(row=0, column=1, padx=(5, 10), pady=(0, 10), sticky="ew")

        # Manage Subscriptions Button
        subscriptions_button = ctk.CTkButton(center_frame, text="Manage Subscriptions", corner_radius=15, command=self.open_subscriptions)
        subscriptions_button.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="ew")

        return self

    def _toggle_currency(self, event=None):
        if cfg.SHOW_DEFAULT_CURRENCY:
            cfg.SHOW_DEFAULT_CURRENCY = False
        else:
            cfg.SHOW_DEFAULT_CURRENCY = True

        self.amount.configure(text=self._get_currency_text())

    def _get_currency_text(self):
        """Return the formatted currency text based on the current state."""
        if cfg.SHOW_DEFAULT_CURRENCY:
            return Exchange.display(to_sym=default_currency())
        else:
            return Exchange.display(to_sym=secondary_currency())

    def open_subscriptions(self):
        self._app.switch_view('subscriptions')

    def open_recieve(self):
        self._app.switch_view('recieve')

    def open_pay(self):
        self._app.switch_view('pay')

    def open_settings(self):
        self._app.switch_view('settings')

    def destroy(self):
        super().destroy()
        for observer in self._element_observers:
            self._rpc_server.detach(observer)
        self._element_observers = []
