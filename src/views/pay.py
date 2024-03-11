import customtkinter as ctk
from src.interfaces.view import View
import config as cfg


class PayView(View):
    def __init__(self, app):
        self._app = app

    def build(self):
        self._app.geometry(cfg.PAY_VIEW_GEOMETRY)

        # Title
        label = self.add(ctk.CTkLabel(self._app, text=' Send To:'))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Back Button
        back_button = self.add(ctk.CTkButton(self._app, text=cfg.BACK_BUTTON_EMOJI, font=(cfg.font, 24), width=35, height=30, command=self.open_main))
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Wallet input box
        # Documentation: https://customtkinter.tomschimansky.com/documentation/widgets/entry
        input_box_for_wallet_or_request = self.add(ctk.CTkEntry(self._app, placeholder_text="Enter a monero payment request or wallet address..."))
        input_box_for_wallet_or_request.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        next_button = self.add(ctk.CTkButton(self._app, text="Paste From Clipboard", command=self.paste_and_next))
        next_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def paste_and_next(self):
        self._app.switch_view('main')  # TODO: UPDATE THIS TO WORK!!!

