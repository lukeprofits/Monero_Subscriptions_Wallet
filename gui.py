import customtkinter
from src.wallet import Wallet
from src.rpc_server import RPCServer

customtkinter.set_default_color_theme("monero_theme.json")


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x200")

        self.sync_status = customtkinter.CTkLabel(self, text="( Sync Status )")
        self.sync_status.place(relx=0.5, rely=0.125, anchor="center") #.pack(side="top", anchor="n", padx=20, pady=20)

        self.settings_button = customtkinter.CTkButton(self, text="Settings", command=self.open_settings)
        self.settings_button.place(relx=0.85, rely=0.125, anchor="center") #.pack(anchor="ne", padx=20, pady=20)

        self.amount = customtkinter.CTkLabel(self, text="$150.00 USD", font=("Helvetica", 48))
        self.amount.place(relx=0.5, rely=0.355, anchor="center") #.pack(padx=20, pady=20)

        # CURRENCY SELECTOR DROPDOWN

        self.recieve_button = customtkinter.CTkButton(self, text="Recieve", command=self.open_recieve)
        self.recieve_button.place(relx=0.333, rely=0.685, anchor="center") #.pack(side="top", padx=20, pady=20)

        self.pay_button = customtkinter.CTkButton(self, text="Pay", command=self.open_pay)
        self.pay_button.place(relx=0.666, rely=0.685, anchor="center") #.pack(side="top", padx=20, pady=20)

        self.subscriptions_button = customtkinter.CTkButton(self, text="                    Manage Subscriptions                    ", command=self.open_subscriptions)
        self.subscriptions_button.place(relx=0.5, rely=0.875, anchor="center") #.pack(side="top", padx=20, pady=20)

        wallet = Wallet()
        rpc_server = RPCServer(wallet)
        rpc_server.start()
        rpc_server.check_if_rpc_server_ready(self.sync_status)

        self.node_selection_button = customtkinter.CTkButton(self, text="Node Selection", command=self.open_node_selection)
        #self.node_selection_button.pack(side="top", padx=20, pady=20)

        self.welcome_message_button = customtkinter.CTkButton(self, text="Welcome Message", command=self.open_welcome_message)
        #self.welcome_message_button.pack(side="top", padx=20, pady=20)

        self.add_payment_request_button = customtkinter.CTkButton(self, text="Add Monero Payment Request", command=self.open_add_payment_request)
        #self.add_payment_request_button.pack(side="top", padx=20, pady=20)

        self.manually_create_payment_request_button = customtkinter.CTkButton(self, text="Manually Create Monero Payment Request", command=self.open_manually_create_payment_request)
        #self.manually_create_payment_request_button.pack(side="top", padx=20, pady=20)

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


    # MANAGE SUBSCRIPTIONS


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


class Recieve(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Recieve Window")
        self.label.pack(padx=20, pady=20)


class Pay(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Pay Window")
        self.label.pack(padx=20, pady=20)


class Settings(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Settings Window")
        self.label.pack(padx=20, pady=20)


class Subscriptions(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="My Subscriptions")
        self.label.pack(padx=20, pady=20)


class NodeSelection(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Node Selection")
        self.label.pack(padx=20, pady=20)


class WelcomeMessage(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Welcome Message")
        self.label.pack(padx=20, pady=20)


class AddPaymentRequest(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Add Payment Request")
        self.label.pack(padx=20, pady=20)


class ManuallyCreatePaymentRequest(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Manually Create Payment Request")
        self.label.pack(padx=20, pady=20)


app = App()
app.mainloop()