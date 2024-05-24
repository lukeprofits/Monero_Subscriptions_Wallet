import customtkinter as ctk
import tkinter
from src.interfaces.view import View
import config as cfg
import styles
import clipboard
import monerorequest
from src.wallet import Wallet

def input_is_valid(input_string):
    if input_string:
        if input_is_valid_monero_wallet(input_string) or input_is_valid_monero_request(input_string):
            return True

    return False


def input_is_valid_monero_wallet(input_string):
    return monerorequest.Check.wallet(wallet_address=input_string, allow_standard=True, allow_integrated_address=True, allow_subaddress=True)


def input_is_valid_monero_request(input_string):
    if 'monero-request:' in input_string:
        # Decode it
        decoded_request = monerorequest.Decode.monero_payment_request_from_code(monero_payment_request=input_string)

        print(decoded_request)

        # Validate fields
        if not monerorequest.Check.name(decoded_request["custom_label"]):
            return False
        if not monerorequest.Check.wallet(decoded_request["sellers_wallet"]):
            return False
        if not monerorequest.Check.amount(decoded_request["amount"]):
            return False
        if not monerorequest.Check.payment_id(decoded_request["payment_id"]):
            return False
        if not monerorequest.Check.start_date(decoded_request["start_date"]):
            return False
        if not monerorequest.Check.days_per_billing_cycle(decoded_request["days_per_billing_cycle"]):
            return False
        if not monerorequest.Check.number_of_payments(decoded_request["number_of_payments"]):
            return False
        if not monerorequest.Check.change_indicator_url(decoded_request["change_indicator_url"]):
            return False

        return True

    else:
        return False


class PayView(View):
    def build(self):
        self._app.geometry(styles.PAY_VIEW_GEOMETRY)

        # Back button and title
        styles.back_and_title(self, ctk, cfg, title='Pay To:')

        # TODO: Can we set the border color through the theme file instead?
        # Input box
        self.payment_input = tkinter.StringVar(self._app, name='payment_input')
        clipboard_contents = clipboard.paste()

        if input_is_valid(input_string=clipboard_contents) and clipboard_contents != Wallet().address:
            self.payment_input.set(clipboard_contents)

            # TODO: refactor this to be better?
            self.input_box_for_wallet_or_request = self.add(ctk.CTkEntry(self._app, textvariable=self.payment_input, font=(styles.font, 12), corner_radius=15, border_color=styles.monero_orange))
        else:
            self.input_box_for_wallet_or_request = self.add(ctk.CTkEntry(self._app, placeholder_text="Enter a monero payment request or wallet address...", font=(styles.font, 12), corner_radius=15, border_color=styles.monero_orange))

        self.input_box_for_wallet_or_request.grid(row=1, column=0, columnspan=3, padx=70, pady=(27.5, 0), sticky="ew")

        # Next button
        next_button = self.add(ctk.CTkButton(self._app, text="Continue", corner_radius=15, command=self.next_button))
        next_button.grid(row=2, column=0, columnspan=3, padx=120, pady=15, sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def wallet_or_request_logic(self, input_string):
        if 'monero-request:' in input_string:
            self._app.switch_view('review_request')
        else:
            cfg.SEND_TO_WALLET = input_string
            # Move to "how much" view
            self._app.switch_view('amount')

    def next_button(self):
        input_string = self.input_box_for_wallet_or_request.get().strip()
        if input_is_valid(input_string=input_string):
            self.wallet_or_request_logic(input_string=input_string)
        else:
            print('Not a Monero Payment Request or wallet address')
