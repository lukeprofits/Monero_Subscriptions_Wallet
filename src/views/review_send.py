import customtkinter as ctk
import monero_usd_price
from src.interfaces.view import View
from src.subscription import Subscription
import config as cfg
import styles
import clipboard
import monerorequest
from datetime import datetime


def clear_temp_payment_info():
    cfg.CURRENT_PAYMENT_REQUEST = ''
    cfg.CURRENT_SEND_CURRENCY = ''
    cfg.CURRENT_SEND_AMOUNT = ''
    cfg.SEND_TO_WALLET = ''


class ReviewSendView(View):
    def build(self):
        # TODO: wrap this whole thing in a try?
        wallet = cfg.SEND_TO_WALLET
        wallet_is_valid = monerorequest.Check.wallet(wallet_address=wallet, allow_standard=True, allow_integrated_address=True, allow_subaddress=True)
        amount_is_valid = True
        currency_is_valid = True

        # TODO: Finish writing all this stuff to validate what we are trying to send & calculate the amount based on currency
        if wallet_is_valid and amount_is_valid and currency_is_valid:
            pass

            # Calculate the amount of Monero that translates to the value of the currency that they want to send in.

            send_amount_of_xmr = 1

        # if send_amount is <= wallet_balance



        self._app.geometry(styles.REVIEW_PROMPT_GEOMETRY)

        # Title
        label = self.add(ctk.CTkLabel(self._app, text='Send Payment?', font=styles.HEADINGS_FONT_SIZE))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=(45, 5), sticky="ew")

        # TODO: show conversion to default currency in ()
        worth_of_xmr_text = ' worth of XMR' if cfg.CURRENT_SEND_CURRENCY.upper() != 'XMR' else ''
        sending_to = self.add(ctk.CTkLabel(self._app, text=f'{cfg.CURRENT_SEND_AMOUNT} {cfg.CURRENT_SEND_CURRENCY}{worth_of_xmr_text} to: {cfg.SEND_TO_WALLET[:5]}...{cfg.SEND_TO_WALLET[-5:]}', font=styles.SUBHEADING_FONT_SIZE))
        sending_to.grid(row=1, column=0, columnspan=3, padx=10, pady=0, sticky="ew")

        # Frame to hold buttons
        center_frame = self.add(ctk.CTkFrame(self._app, ))
        center_frame.grid(row=3, column=0, columnspan=3, padx=0, pady=15, sticky="nsew")
        center_frame.columnconfigure([0, 1, 2, 3, 4, 5], weight=1)

        # Cancel button
        cancel_button = self.add(ctk.CTkButton(center_frame, text="Cancel", corner_radius=15, command=self.cancel_button))
        cancel_button.grid(row=0, column=2, padx=(10, 5), pady=0, sticky="e")

        # Confirm button
        confirm_button = self.add(ctk.CTkButton(center_frame, text="Send", corner_radius=15, command=self.confirm_button))
        confirm_button.grid(row=0, column=3, padx=(5, 10), pady=0, sticky="w")

        return self

    def cancel_button(self):
        clear_temp_payment_info()
        self.open_main()

    def confirm_button(self):
        # TODO: Make send payment work
        # Send the payment

        # Confirm if it worked or not (if not, let them retry)

        clear_temp_payment_info()

        self.open_main()

    def open_main(self):
        self._app.switch_view('main')
