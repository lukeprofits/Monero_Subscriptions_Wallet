import customtkinter as ctk
from src.interfaces.view import View
from src.subscription import Subscription
import config as cfg
import styles
import monerorequest
from datetime import datetime


class ReviewRequestView(View):
    def build(self):
        # TODO: wrap this whole thing in a try?
        decoded_request = monerorequest.decode_monero_payment_request(self._app.views['pay'].payment_input.get())

        if decoded_request["number_of_payments"] == 0:
            payment_count = f'every {decoded_request["days_per_billing_cycle"]} days until canceled'
        elif decoded_request["number_of_payments"] == 1:
            payment_count = 'one-time'
        else:
            payment_count = f'every {decoded_request["days_per_billing_cycle"]} days until {decoded_request["number_of_payments"]} payments have been made'

        worth_of_xmr = ' worth of XMR' if decoded_request["currency"].upper() != 'XMR' else ''

        self._app.geometry(styles.REVIEW_REQUEST_VIEW_GEOMETRY)

        # Back button and title
        styles.back_and_title(self, ctk, cfg, title=' Add Payment Request?')

        # Custom Label
        custom_label = self.add(ctk.CTkLabel(self._app, text=f'{decoded_request["custom_label"][:80]}:', font=styles.SUBHEADING_FONT_SIZE))
        custom_label.grid(row=1, column=0, columnspan=3, padx=10, pady=(10, 0), sticky="ew")

        # TODO: show conversion to default currency in ()
        amount_label = self.add(ctk.CTkLabel(self._app, text=f'{decoded_request["amount"]} {decoded_request["currency"]}{worth_of_xmr} billed {payment_count}', font=styles.BODY_FONT_SIZE))
        amount_label.grid(row=2, column=0, columnspan=3, padx=10, pady=0, sticky="ew")

        # Start Date  decoded_request["start_date"]
        starting_on = self.add(ctk.CTkLabel(self._app, text=f'First payment due: {datetime.strptime(decoded_request["start_date"].split("T")[0], "%Y-%m-%d").strftime("%B %-d, %Y")}', font=styles.BODY_FONT_SIZE))
        starting_on.grid(row=3, column=0, columnspan=3, padx=10, pady=0, sticky="ew")

        # Sellers Wallet
        sellers_wallet_label = self.add(ctk.CTkLabel(self._app, text=f'Paying To: {decoded_request["sellers_wallet"][:5]}...{decoded_request["sellers_wallet"][-5:]}', font=styles.BODY_FONT_SIZE))
        sellers_wallet_label.grid(row=4, column=0, columnspan=3, padx=10, pady=0, sticky="ew")

        # TODO: Have window adjust automatically if we even display this.
        '''
        if decoded_request["change_indicator_url"]:
            sellers_wallet_label = self.add(ctk.CTkLabel(self._app, text=f'(Seller may request changes to this. If they do, payments will be paused until you approve them.)', font=styles.BODY_FONT_SIZE))
            sellers_wallet_label.grid(row=5, column=0, columnspan=3, padx=10, pady=0, sticky="ew")
        '''

        # Frame to hold buttons
        center_frame = self.add(ctk.CTkFrame(self._app, ))
        center_frame.grid(row=6, column=0, columnspan=3, padx=0, pady=10, sticky="nsew")
        center_frame.columnconfigure([0, 1], weight=1)  # Frame will span 3 columns but contain two columns (0 and 1)

        # Cancel button
        cancel_button = self.add(ctk.CTkButton(center_frame, text="No Thanks", command=self.cancel_button))
        cancel_button.grid(row=0, column=0, padx=(10, 5), pady=(0, 10), sticky="ew")

        # Confirm button
        confirm_text = "Pay Now" if decoded_request["number_of_payments"] == 1 else "Subscribe"
        confirm_button = self.add(ctk.CTkButton(center_frame, text=confirm_text, command=self.confirm_button))
        confirm_button.grid(row=0, column=1, padx=(5, 10), pady=(0, 10), sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def cancel_button(self):
        self.open_main()

    def confirm_button(self):
        cfg.config_file.add_subscription(Subscription(**Subscription.decode(self._app.views['pay'].payment_input.get())))
        self._app.switch_view('subscriptions')
