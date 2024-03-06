import customtkinter as ctk
from src.interfaces.view import View

class RecieveView(View):
    def __init__(self, app):
        self._app = app

    def build(self):
        self.window_label()

    def window_label(self):
        label = self.add(ctk.CTkLabel(self._app, text="Recieve Window"))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        return label