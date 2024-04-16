import customtkinter as ctk
from src.interfaces.view import View
from src.subscription import Subscription
import config as cfg
import monerorequest
from datetime import datetime

class ReviewRequestView(View):
    def build(self):
        # TODO: wrap this whole thing in a try?
        decoded_request = monerorequest.decode_monero_payment_request(cfg.CURRENT_PAYMENT_REQUEST)

        if decoded_request["number_of_payments"] == 0:
            payment_count = f'every {decoded_request["days_per_billing_cycle"]} days until canceled'
        elif decoded_request["number_of_payments"] == 1:
            payment_count = 'one-time'
        else:
            payment_count = f'every {decoded_request["days_per_billing_cycle"]} days until {decoded_request["number_of_payments"]} payments have been made'

        worth_of_xmr = ' worth of XMR' if decoded_request["currency"].upper() != 'XMR' else ''

        self._app.geometry(cfg.REVIEW_REQUEST_VIEW_GEOMETRY)

        # Back button and title
        cfg.back_and_title(self, ctk, cfg, title=' Add Payment Request?')

        # Custom Label
        custom_label = self.add(ctk.CTkLabel(self._app, text=f'{decoded_request["custom_label"][:80]}:', font=cfg.SUBHEADING_FONT_SIZE))
        custom_label.grid(row=1, column=0, columnspan=3, padx=10, pady=0, sticky="ew")

        # TODO: show conversion to default currency in ()
        amount_label = self.add(ctk.CTkLabel(self._app, text=f'{decoded_request["amount"]} {decoded_request["currency"]}{worth_of_xmr} billed {payment_count}', font=cfg.BODY_FONT_SIZE))
        amount_label.grid(row=2, column=0, columnspan=3, padx=10, pady=0, sticky="ew")

        # Start Date  decoded_request["start_date"]
        starting_on = self.add(ctk.CTkLabel(self._app, text=f'First payment due: {datetime.strptime(decoded_request["start_date"].split("T")[0], "%Y-%m-%d").strftime("%B %-d, %Y")}', font=cfg.BODY_FONT_SIZE))
        starting_on.grid(row=3, column=0, columnspan=3, padx=10, pady=0, sticky="ew")

        # Sellers Wallet
        sellers_wallet_label = self.add(ctk.CTkLabel(self._app, text=f'Paying To: {decoded_request["sellers_wallet"][:5]}...{decoded_request["sellers_wallet"][-5:]}', font=cfg.BODY_FONT_SIZE))
        sellers_wallet_label.grid(row=4, column=0, columnspan=3, padx=10, pady=0, sticky="ew")

        # TODO: Have window adjust automatically if we even display this.
        '''
        if decoded_request["change_indicator_url"]:
            sellers_wallet_label = self.add(ctk.CTkLabel(self._app, text=f'(Seller may request changes to this. If they do, payments will be paused until you approve them.)', font=cfg.BODY_FONT_SIZE))
            sellers_wallet_label.grid(row=5, column=0, columnspan=3, padx=10, pady=0, sticky="ew")
        '''

        # Frame to hold buttons
        center_frame = self.add(ctk.CTkFrame(self._app, ))
        center_frame.grid(row=6, column=0, columnspan=3, padx=0, pady=10, sticky="nsew")
        center_frame.columnconfigure([0, 1], weight=1)  # Frame will span 3 columns but contain two columns (0 and 1)

        # Cancel button
        cancel_button = self.add(ctk.CTkButton(center_frame, text="Reject", command=self.cancel_button))
        cancel_button.grid(row=0, column=0, padx=(10, 5), pady=(0, 10), sticky="ew")

        # Confirm button
        confirm_button = self.add(ctk.CTkButton(center_frame, text="Approve", command=self.confirm_button))
        confirm_button.grid(row=0, column=1, padx=(5, 10), pady=(0, 10), sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def cancel_button(self):
        cfg.CURRENT_PAYMENT_REQUEST = ''
        self.open_main()

    def confirm_button(self):
        cfg.config_file.add_subscription(Subscription(**Subscription.decode(cfg.CURRENT_PAYMENT_REQUEST)))
        cfg.CURRENT_PAYMENT_REQUEST = ''
        self._app.switch_view('subscriptions')


#4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2D
#monero-request:1:H4sIAAAAAAAC/y2OX2+CMBTFv0uf1VSsirzpMBiTGQao05emlE7r2kL6B8Vl333FLLnJzfmdm3vODyCydsqCCMARHIMBoFeiLgxzVXFKbK2x08K7veO0Zop2Xu3z+AWMrSUWpGT9ScGM9bQincEN07jkQnB1wbSjgoFoAgdAOVl6p/7CDekkU9aAyON/gXnl3yBEZ2M4Y+GcIMbCvpNhQjBt8J343XdF0+1t/zgmK/ksl4tNmNspjYM0OQRb1zbt5/OEdDtr3nRxzIvT9JrdyfKWb/ni/Dg+rnUsM75RqZT1R5jJ8/Lw7r53ydqs012eFsGqj7REW1wR65uDAAZoCCdDOC8gjF4zghCewe8f/GxR8kABAAA=