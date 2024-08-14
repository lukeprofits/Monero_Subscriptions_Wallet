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
        styles.back_and_title(self, ctk, cfg, title='Payment Request Created:')

        # TODO: Can we set the border color through the theme file instead?

        # Generated Payment Request To Copy
        self.pr = "monero-request:1:H4sIAAAAAAAC/y1QXU/DMAz8KyjPG0o/ttK+tWuHBAKJrcDYS5Q07hqRJlOSDlrEfyedkCzZd2edT/5BtNeDcihDAb7FGC1Q01F1AiIUFw112pDBSC/PymAMqGb06HVfXgnrdE8kZTCvlHABqc9gbkqtqBNa+R1OR0s8R5iQUqgTacZGAsoivEBq6JlXdEvOdOxBOYsyT/8DIrg3je9YG4dxgoEFIU9Tb2lBSjCWfFHf5+hx7qLDylzexnOt21M/wHNq0xdnJr6DVTHA1tjP/CiCpNAfrJtGq6dJP22L9fSu6kd+v1nn31XOqmrVTNtd1Pnpgdk+7jZwCPfzSUeNI5w6nxyFOIyWAV6GSY1xdi3/OnxEv3/sOZmDTwEAAA=="
        self.pr_id = "9fc88080d1d5dc09"

        main_text = self.add(ctk.CTkLabel(self._app, text="It’s on your clipboard. Use unique payment requests for each", font=styles.BODY_FONT_SIZE))
        main_text.grid(row=1, column=0, columnspan=3, padx=10, pady=(5, 0), sticky='ew')

        second_text = self.add(ctk.CTkLabel(self._app, text="buyer if you want to know who to credit with a purchase.", font=styles.BODY_FONT_SIZE))
        second_text.grid(row=2, column=0, columnspan=3, padx=10, pady=0, sticky='ew')

        third_text = self.add(ctk.CTkLabel(self._app, text=f"Only you can see the payment ID: {self.pr_id}", font=styles.BODY_FONT_SIZE))
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
        clipboard.copy(self.pr)
        print('Copied Payment Request!')

    def copy_payment_id(self):
        print('Copied Payment ID!')
        clipboard.copy(self.pr_id)