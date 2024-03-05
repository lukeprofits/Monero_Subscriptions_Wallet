import customtkinter as ctk
from src.interfaces.view import View

class SubscriptionsView(View):
    def __init__(self, app):
        self._app = app

    def build(self):
        self.label()

    def label(self):
        label = self.add(ctk.CTkLabel(self._app, text="My Subscriptions"))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        return label