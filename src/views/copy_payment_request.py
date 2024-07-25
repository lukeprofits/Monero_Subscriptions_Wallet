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
        self._app.geometry(styles.COPY_PAYMENT_REQUEST_VIEW_GEOMETRY)

        # Back button and title
        styles.back_and_title(self, ctk, cfg, title='Copy Payment Request:')

        # TODO: Can we set the border color through the theme file instead?

        # Generated Payment Request To Copy
        #pr = "monero-request:1:H4sIAAAAAAAC/y1QXU/DMAz8KyjPG0o/ttK+tWuHBAKJrcDYS5Q07hqRJlOSDlrEfyedkCzZd2edT/5BtNeDcihDAb7FGC1Q01F1AiIUFw112pDBSC/PymAMqGb06HVfXgnrdE8kZTCvlHABqc9gbkqtqBNa+R1OR0s8R5iQUqgTacZGAsoivEBq6JlXdEvOdOxBOYsyT/8DIrg3je9YG4dxgoEFIU9Tb2lBSjCWfFHf5+hx7qLDylzexnOt21M/wHNq0xdnJr6DVTHA1tjP/CiCpNAfrJtGq6dJP22L9fSu6kd+v1nn31XOqmrVTNtd1Pnpgdk+7jZwCPfzSUeNI5w6nxyFOIyWAV6GSY1xdi3/OnxEv3/sOZmDTwEAAA=="
        payment_request_text = self.add(ctk.CTkButton(self._app, text="Payment ID: 9fc88080d1d5dc09", font=styles.SUBHEADING_FONT_SIZE, fg_color='transparent'))
        payment_request_text.grid(row=1, column=0, columnspan=3, padx=(5, 10), pady=(27.5, 0), sticky='ew')

        copy_request_button = self.add(ctk.CTkButton(self._app, text="Copy Payment Request", corner_radius=15, command=self.copy_payment_request))
        copy_request_button.grid(row=2, column=0, columnspan=3, padx=160, pady=(17.5, 0), sticky="ew")

        #copy_payment_id_button = self.add(ctk.CTkButton(self._app, text="Copy Payment ID", corner_radius=15, command=self.copy_payment_request))
        #copy_payment_id_button.grid(row=3, column=0, columnspan=3, padx=70, pady=10, sticky="ew")

        # Next button
        #next_button = self.add(ctk.CTkButton(self._app, text="Done", corner_radius=15, command=self.open_main))
        #next_button.grid(row=4, column=0, columnspan=3, padx=120, pady=15, sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def copy_payment_request(self):
        print('Copied Payment Request!')
        self._app.switch_view('main')