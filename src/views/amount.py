import customtkinter as ctk
from src.interfaces.view import View
import config as cfg


class AmountView(View):
    def build(self):
        self._app.geometry(cfg.AMOUNT_VIEW_GEOMETRY)

        # Title
        label = self.add(ctk.CTkLabel(self._app, text=' Amount:'))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Back Button
        back_button = self.add(ctk.CTkButton(self._app, text=cfg.BACK_BUTTON_EMOJI, font=(cfg.font, 24), width=35, height=30, command=self.open_main))
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Wallet
        wallet = self.add(ctk.CTkLabel(self._app, text=f'Sending to wallet: {cfg.SEND_TO_WALLET[:4]}... ...{cfg.SEND_TO_WALLET[-4:]}'))
        wallet.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Input box
        self.input_box_for_amount = self.add(ctk.CTkEntry(self._app, placeholder_text="Enter an amount"))
        self.input_box_for_amount.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

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
