import customtkinter as ctk
from src.interfaces.view import View
import config as cfg


class AmountView(View):
    def build(self):
        self._app.geometry(cfg.AMOUNT_VIEW_GEOMETRY)

        # Back button and title
        cfg.back_and_title(self, ctk, cfg, title=' Amount:')

        # Input box
        self.input_box_for_amount = self.add(ctk.CTkEntry(self._app, placeholder_text="Enter an amount"))
        self.input_box_for_amount.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Wallet
        wallet = self.add(ctk.CTkLabel(self._app, text=f'To Wallet: {cfg.SEND_TO_WALLET[:5]}...{cfg.SEND_TO_WALLET[-5:]}'))  # TODO: Make it so that they can click the wallet to go back to "pay" view
        wallet.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Send button
        send_button = self.add(ctk.CTkButton(self._app, text="Send", command=self.send_button))
        send_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def send_button(self):
        # Send function
        wallet = cfg.SEND_TO_WALLET
        amount = self.input_box_for_amount.get().strip()
        self._app.switch_view('main')
