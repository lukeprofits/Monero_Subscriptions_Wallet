import customtkinter as ctk
from src.interfaces.view import View

class SettingsView(View):
    def __init__(self, app):
        self._app = app

    def build(self):
        self.label()
        self.node_selection_button()
        self.welcome_message_button()
        self.add_payment_request_button()
        self.manually_create_payment_request_button()

    def label(self):
        label = self.add(ctk.CTkLabel(self._app, text="Settings Window"))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        return label

    def node_selection_button(self):
        self.node_selection_button = self.add(ctk.CTkButton(self._app, text="Node Selection", command=self.open_node_selection))
        self.node_selection_button.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    def welcome_message_button(self):
        self.welcome_message_button = self.add(ctk.CTkButton(self._app, text="Welcome Message", command=self.open_welcome_message))
        self.welcome_message_button.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    def add_payment_request_button(self):
        self.add_payment_request_button = self.add(ctk.CTkButton(self._app, text="Add Monero Payment Request", command=self.open_add_payment_request))
        self.add_payment_request_button.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    def manually_create_payment_request_button(self):
        self.manually_create_payment_request_button = self.add(ctk.CTkButton(self._app, text="Manually Create Monero Payment Request", command=self.open_manually_create_payment_request))
        self.manually_create_payment_request_button.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    def open_node_selection(self):
        self._app.switch_view('node_selection')

    def open_welcome_message(self):
        self._app.switch_view('welcome_message')

    def open_add_payment_request(self):
        self._app.switch_view('payment_request')

    def open_manually_create_payment_request(self):
        self._app.switch_view('manual_payment')
