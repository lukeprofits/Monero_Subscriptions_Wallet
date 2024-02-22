import customtkinter

customtkinter.set_default_color_theme("monero_theme.json")


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x800")

        self.deposit_button = customtkinter.CTkButton(self, text="Deposit", command=self.open_deposit)
        self.deposit_button.pack(side="top", padx=20, pady=20)

        self.send_button = customtkinter.CTkButton(self, text="Send", command=self.open_send)
        self.send_button.pack(side="top", padx=20, pady=20)

        self.subscriptions_button = customtkinter.CTkButton(self, text="My Subscriptions", command=self.open_subscriptions)
        self.subscriptions_button.pack(side="top", padx=20, pady=20)

        self.settings_button = customtkinter.CTkButton(self, text="Settings", command=self.open_settings)
        self.settings_button.pack(side="top", padx=20, pady=20)

        self.node_selection_button = customtkinter.CTkButton(self, text="Node Selection", command=self.open_node_selection)
        self.node_selection_button.pack(side="top", padx=20, pady=20)

        self.welcome_message_button = customtkinter.CTkButton(self, text="Welcome Message", command=self.open_welcome_message)
        self.welcome_message_button.pack(side="top", padx=20, pady=20)

        self.add_payment_request_button = customtkinter.CTkButton(self, text="Add Monero Payment Request", command=self.open_add_payment_request)
        self.add_payment_request_button.pack(side="top", padx=20, pady=20)

        self.manually_create_payment_request_button = customtkinter.CTkButton(self, text="Manually Create Monero Payment Request", command=self.open_manually_create_payment_request)
        self.manually_create_payment_request_button.pack(side="top", padx=20, pady=20)

        self.toplevel_window = None

    def open_deposit(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Deposit(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def open_send(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Send(self)  # create window if its None or destroyed
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


class Deposit(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Deposit Window")
        self.label.pack(padx=20, pady=20)


class Send(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="Send Window")
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