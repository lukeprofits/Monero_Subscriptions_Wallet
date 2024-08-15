import customtkinter as ctk
import tkinter

from src.exchange import Exchange
from src.interfaces.view import View
from config import default_currency
import config as cfg
import styles
import clipboard
import monerorequest
from src.wallet import Wallet


def insert_newlines(input_string, characters_per_line):
    result = ''
    for i in range(0, len(input_string), characters_per_line):
        result += input_string[i:i+characters_per_line] + '\n'
    return result


class CopyPaymentRequestView(View):
    def build(self):
        self.payment_request = clipboard.paste()
        print(monerorequest.decode_monero_payment_request(self.payment_request))
        self.payment_request_payment_id = monerorequest.decode_monero_payment_request(self.payment_request)["payment_id"]

        self._app.geometry(styles.COPY_PAYMENT_REQUEST_VIEW_GEOMETRY)

        # Back button and title
        styles.back_and_title(self, ctk, cfg, title='Payment Request Created:')

        # TODO: Can we set the border color through the theme file instead?

        # Generated Payment Request To Copy
        main_text = self.add(ctk.CTkLabel(self._app, text="It’s on your clipboard. Use unique payment requests for each", font=styles.BODY_FONT_SIZE))
        main_text.grid(row=1, column=0, columnspan=3, padx=10, pady=(5, 0), sticky='ew')

        second_text = self.add(ctk.CTkLabel(self._app, text="buyer if you want to know who to credit with a purchase.", font=styles.BODY_FONT_SIZE))
        second_text.grid(row=2, column=0, columnspan=3, padx=10, pady=0, sticky='ew')

        third_text = self.add(ctk.CTkLabel(self._app, text=f"Only you can see the payment ID: {self.payment_request_payment_id}", font=styles.BODY_FONT_SIZE))
        third_text.grid(row=3, column=0, columnspan=3, padx=10, pady=0, sticky='ew')

        # Frame to hold buttons
        center_frame = self.add(ctk.CTkFrame(self._app, ))
        center_frame.grid(row=4, column=0, columnspan=3, padx=0, pady=(10, 0), sticky="nsew")
        center_frame.columnconfigure([0, 1, 2, 3], weight=1)

        copy_payment_id_button = self.add(ctk.CTkButton(center_frame, text="Copy Payment ID", corner_radius=15, command=self.copy_payment_id))
        copy_payment_id_button.grid(row=0, column=1, padx=(10, 5), pady=0, sticky="ew")

        copy_request_button = self.add(ctk.CTkButton(center_frame, text="Copy Payment Request", corner_radius=15, command=self.copy_payment_request))
        copy_request_button.grid(row=0, column=2, padx=(5, 10), pady=0, sticky="ew")

        # Next button
        next_button = self.add(ctk.CTkButton(self._app, text="Finished", corner_radius=15, command=self.open_main))
        next_button.grid(row=5, column=0, columnspan=3, padx=120, pady=(10, 15), sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def copy_payment_request(self):
        print('Copied Payment Request!')
        clipboard.copy(self.payment_request)

    def copy_payment_id(self):
        clipboard.copy(self.payment_request_payment_id)
        print('Copied Payment ID!')