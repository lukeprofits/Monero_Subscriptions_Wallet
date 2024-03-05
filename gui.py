import random

import customtkinter as ctk

import subscription_functions
import config as cfg

from src.wallet import Wallet
from src.rpc_server import RPCServer
from src.observers.rpc_server_status_observer import RPCServerStatusObserver
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

        # Sync Status
        self.sync_status = ctk.CTkLabel(self, text="( Sync Status )")
        self.sync_status.grid(row=0, column=0, columnspan=3, padx=0, pady=10, sticky="ew")

        # Settings Button
        self.settings_button = ctk.CTkButton(self, text="⚙", font=("Helvetica", 24), width=35, height=30, command=self.open_settings)
        self.settings_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

        # Amount
        self.amount = ctk.CTkLabel(self, text="$150.00 USD", font=("Helvetica", 48))
        self.amount.grid(row=1, column=0, columnspan=3, padx=10, pady=0, sticky="nsew")

        # Frame to hold buttons
        center_frame = ctk.CTkFrame(self,)
        center_frame.grid(row=3, column=0, columnspan=3, padx=0, pady=10, sticky="nsew")
        center_frame.columnconfigure([0, 1], weight=1)  # Frame will span 3 columns but contain two columns (0 and 1)

        '''  # Commented out while designing GUI
        wallet = Wallet()
        self.rpc_server = RPCServer(wallet)
        observer = RPCServerStatusObserver(self.sync_status)
        self.rpc_server.attach(observer)
        self.rpc_server.start()
        self.rpc_server.check_if_rpc_server_ready()
        #'''

        # Receive Button
        self.receive_button = ctk.CTkButton(center_frame, text="Receive", command=self.open_recieve)
        self.receive_button.grid(row=0, column=0, padx=(10, 5), pady=(0, 10), sticky="ew")

        # Pay Button
        self.pay_button = ctk.CTkButton(center_frame, text="Pay", command=self.open_pay)
        self.pay_button.grid(row=0, column=1, padx=(5, 10), pady=(0, 10), sticky="ew")

        # Manage Subscriptions Button
        self.subscriptions_button = ctk.CTkButton(center_frame, text="Manage Subscriptions", command=self.open_subscriptions)
        self.subscriptions_button.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="ew")


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
        self.destroy()
        self.rpc_server.kill()


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
        self.geometry("400x600")

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

        self.set_currency_button = ctk.CTkButton(self, text="Set Currency", command=self.open_set_currency)
        self.set_currency_button.pack(side="top", padx=20, pady=20)

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

    def open_set_currency(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = SetCurrency(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it


class Subscriptions(ctk.CTkToplevel):

    # Update subscriptions in config
    subscription_functions.get_subscriptions_from_file()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x600")

        #'''  # Comment out to make NOT fullscreen.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # '''

        self.my_frame = SubscriptionsScrollableFrame(master=self, width=300, height=200, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, sticky="nsew")


class SubscriptionsScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.title = ctk.CTkLabel(self, text=" My Subscriptions:", font=("Helvetica", 20))
        self.title.pack(padx=10, pady=(20, 0))

        self.separator = ctk.CTkFrame(self, height=2)
        self.separator.pack(fill='x', padx=10, pady=20)

        if cfg.subscriptions:
            for sub in cfg.subscriptions:
                self.subscription_name = ctk.CTkLabel(self, text=f"{sub["custom_label"]}")
                self.subscription_name.pack()

                self.subscription_price = ctk.CTkLabel(self, text=f"{sub["amount"]} {sub["currency"]}")
                self.subscription_price.pack()

                # TODO: Make this accurate. Right now it just shows billing cycle
                self.subscription_renews_in = ctk.CTkLabel(self, text=f"Renews In {sub["days_per_billing_cycle"]} Days")
                self.subscription_renews_in.pack()

                self.subscription_cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_subscription)
                self.subscription_cancel_button.pack(pady=10)

                # Separator
                separator = ctk.CTkFrame(self, height=2)  # bg_color="#ffffff" if needed
                separator.pack(fill='x', padx=10, pady=20)
        else:
            self.no_subs_text = ctk.CTkLabel(self, text="You haven't added any subscriptions.", )
            self.no_subs_text.pack(padx=10, pady=(20, 0))

            # TODO: Have this close the window, open "Pay".
            self.subscription_cancel_button = ctk.CTkButton(self, text="Add Subscription", command=self.cancel_subscription)
            self.subscription_cancel_button.pack(pady=10)

            self.separator = ctk.CTkFrame(self, height=2)
            self.separator.pack(fill='x', padx=10, pady=20)


    # TODO: Make this do something.
    def cancel_subscription(self):
            pass




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


class SetCurrency(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x300")

        def default_currency_selector_callback(choice):
            global DEFAULT_CURRENCY
            print(DEFAULT_CURRENCY)
            DEFAULT_CURRENCY = choice
            print("User chose:", choice)
            print("Now set to:", DEFAULT_CURRENCY)

        def secondary_currency_selector_callback(choice):
            global SECONDARY_CURRENCY
            print(SECONDARY_CURRENCY)
            print("User chose:", choice)
            SECONDARY_CURRENCY = choice
            print("Now set to:", SECONDARY_CURRENCY)

        set_currency_window_text = """
        Set Default Currency:
        
        The currency that you select will be shown by default. 
        
        To toggle to the the Monero amount in the main window, simply click it."""

        self.label = ctk.CTkLabel(self, text=set_currency_window_text)
        self.label.pack(padx=20, pady=20)

        # Default Currency
        self.selected_currency = ctk.StringVar(value=DEFAULT_CURRENCY)
        self.currency_selector = ctk.CTkOptionMenu(self, values=CURRENCY_OPTIONS, command=default_currency_selector_callback, variable=self.selected_currency)
        self.currency_selector.pack(padx=20, pady=20)

        # Secondary Currency
        self.selected_currency = ctk.StringVar(value=SECONDARY_CURRENCY)
        self.currency_selector = ctk.CTkOptionMenu(self, values=CURRENCY_OPTIONS, command=secondary_currency_selector_callback, variable=self.selected_currency)
        self.currency_selector.pack(padx=20, pady=20)




app = App()
app.protocol("WM_DELETE_WINDOW", app.shutdown_steps)
app.mainloop()