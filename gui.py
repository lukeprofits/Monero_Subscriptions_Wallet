import customtkinter as ctk
from src.wallet import Wallet
from src.rpc_server import RPCServer
from src.observers.rpc_server_status_observer import RPCServerStatusObserver
ctk.set_default_color_theme("monero_theme.json")

# VARIABLES TO MOVE TO CONFIG
CURRENCY_OPTIONS = ["USD", "XMR", "BTC", "EUR", "GBP"]  # Is there a library for pulling these in automatically?
SELECTED_CURRENCY = CURRENCY_OPTIONS[0]

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x260")
        # 3 columns 2 rows

        def currency_selector_callback(choice):
            SELECTED_CURRENCY = choice
            print("User chose:", choice)
            print(SELECTED_CURRENCY)

        # Configure the main window grid for spacing and alignment
        self.columnconfigure([0, 1, 2], weight=1)

        # Sync Status
        self.sync_status = ctk.CTkLabel(self, text="( Sync Status )")
        self.sync_status.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Settings Button
        self.settings_button = ctk.CTkButton(self, text="⚙", font=("Helvetica", 24), width=35, height=30, command=self.open_settings)
        self.settings_button.grid(row=0, column=2, padx=20, pady=10, sticky="e")

        # Amount
        self.amount = ctk.CTkLabel(self, text="$150.00 USD", font=("Helvetica", 48))
        self.amount.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # TODO: Finish properly aligning this in the window
        # Selected Currency
        self.selected_currencey = ctk.StringVar(value=SELECTED_CURRENCY)
        self.currency_selector = ctk.CTkOptionMenu(self, width=25, values=CURRENCY_OPTIONS, command=currency_selector_callback, variable=self.selected_currencey)
        self.currency_selector.grid(row=2, column=1)

        # Frame to hold buttons
        center_frame = ctk.CTkFrame(self,)
        center_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        center_frame.columnconfigure([0, 1, 2], weight=1)

        wallet = Wallet()
        self.rpc_server = RPCServer(wallet)
        observer = RPCServerStatusObserver(self.sync_status)
        self.rpc_server.attach(observer)
        self.rpc_server.start()
        self.rpc_server.check_if_rpc_server_ready()

        # Receive Button
        self.receive_button = ctk.CTkButton(center_frame, text="Receive", command=self.open_recieve)
        self.receive_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        # Selector Button
        #self.receive_button = ctk.CTkButton(center_frame, text="XMR", width=10, command=self.open_recieve)
        #self.receive_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Pay Button
        self.pay_button = ctk.CTkButton(center_frame, text="Pay", command=self.open_pay)
        self.pay_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        # Manage Subscriptions Button
        self.subscriptions_button = ctk.CTkButton(center_frame, text="Manage Subscriptions", command=self.open_subscriptions)
        self.subscriptions_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")


        self.toplevel_window = None

    def open_recieve(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Recieve(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def open_pay(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Pay(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def open_subscriptions(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Subscriptions(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def open_settings(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Settings(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def shutdown_steps(self):
        self.rpc_server.kill()
        self.destroy()

class Recieve(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="Recieve Window")
        self.label.pack(padx=20, pady=20)


class Pay(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="Pay Window")
        self.label.pack(padx=20, pady=20)


class Settings(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="Settings Window")
        self.label.pack(padx=20, pady=20)

        self.node_selection_button = ctk.CTkButton(self, text="Node Selection", command=self.open_node_selection)
        self.node_selection_button.pack(side="top", padx=20, pady=20)

        self.welcome_message_button = ctk.CTkButton(self, text="Welcome Message", command=self.open_welcome_message)
        self.welcome_message_button.pack(side="top", padx=20, pady=20)

        self.add_payment_request_button = ctk.CTkButton(self, text="Add Monero Payment Request", command=self.open_add_payment_request)
        self.add_payment_request_button.pack(side="top", padx=20, pady=20)

        self.manually_create_payment_request_button = ctk.CTkButton(self, text="Manually Create Monero Payment Request", command=self.open_manually_create_payment_request)
        self.manually_create_payment_request_button.pack(side="top", padx=20, pady=20)

        self.toplevel_window = None

    def open_node_selection(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = NodeSelection(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def open_welcome_message(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = WelcomeMessage(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def open_add_payment_request(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = AddPaymentRequest(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def open_manually_create_payment_request(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ManuallyCreatePaymentRequest(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it


class Subscriptions(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = ctk.CTkLabel(self, text="My Subscriptions")
        self.label.pack(padx=20, pady=20)


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