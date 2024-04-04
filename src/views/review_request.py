import customtkinter as ctk
from src.interfaces.view import View
from src.all_subscriptions import AllSubscriptions
from src.subscription import Subscription
import config as cfg
import clipboard
import monerorequest


class ReviewRequestView(View):
    def build(self):
        # TODO: wrap this whole thing in a try?
        decoded_request = monerorequest.decode_monero_payment_request(cfg.CURRENT_PAYMENT_REQUEST)

        if decoded_request["number_of_payments"] == 0:
            payment_count = 'A recurring subscription of'
        elif decoded_request["number_of_payments"] == 1:
            payment_count = 'A one-time payment of'
        else:
            payment_count = f'{decoded_request["number_of_payments"]}x payments of'

        worth_of_xmr = ' worth of XMR' if decoded_request["currency"].upper() != 'XMR' else ''

        self._app.geometry(cfg.PAY_VIEW_GEOMETRY)

        # Back button and title
        cfg.back_and_title(self, ctk, cfg, title=' Review Payment Request:')

        # Custom Label
        custom_label = self.add(ctk.CTkLabel(self._app, text=f'For: {decoded_request["custom_label"][:80]}', font=cfg.SUBHEADING_FONT_SIZE))
        custom_label.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # TODO: show conversion to default currency in ()
        amount_label = self.add(ctk.CTkLabel(self._app, text=f'Cost: {payment_count} {decoded_request["amount"]} {decoded_request["currency"]}{worth_of_xmr}', font=cfg.SUBHEADING_FONT_SIZE))
        amount_label.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Start Date  decoded_request["start_date"]
        starting_on = self.add(ctk.CTkLabel(self._app, text=f'Starting On: {decoded_request["start_date"]} and billing every {decoded_request["days_per_billing_cycle"]} days', font=cfg.SUBHEADING_FONT_SIZE))
        starting_on.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Sellers Wallet
        sellers_wallet_label = self.add(ctk.CTkLabel(self._app, text=f'Paying To: {decoded_request["sellers_wallet"][:5]}...{decoded_request["sellers_wallet"][-5:]}', font=cfg.SUBHEADING_FONT_SIZE))
        sellers_wallet_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        if decoded_request["change_indicator_url"]:
            sellers_wallet_label = self.add(ctk.CTkLabel(self._app, text=f'(Seller may request changes to this. If they do, payments will be paused until you approve them.)', font=cfg.SUBHEADING_FONT_SIZE))
            sellers_wallet_label.grid(row=4, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Cancel button
        cancel_button = self.add(ctk.CTkButton(self._app, text="Cancel", command=self.cancel_button))
        cancel_button.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Confirm button
        confirm_button = self.add(ctk.CTkButton(self._app, text="Confirm", command=self.confirm_button))
        confirm_button.grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def cancel_button(self):
        cfg.CURRENT_PAYMENT_REQUEST = ''
        self.open_main()

    def confirm_button(self):
        subs = AllSubscriptions()
        subs.add(Subscription(**Subscription.decode(cfg.CURRENT_PAYMENT_REQUEST)))
        cfg.CURRENT_PAYMENT_REQUEST = ''
        self._app.switch_view('subscriptions')


#4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2D
#monero-request:1:H4sIAAAAAAAC/y2OX2+CMBTFv0uf1VSsirzpMBiTGQao05emlE7r2kL6B8Vl333FLLnJzfmdm3vODyCydsqCCMARHIMBoFeiLgxzVXFKbK2x08K7veO0Zop2Xu3z+AWMrSUWpGT9ScGM9bQincEN07jkQnB1wbSjgoFoAgdAOVl6p/7CDekkU9aAyON/gXnl3yBEZ2M4Y+GcIMbCvpNhQjBt8J343XdF0+1t/zgmK/ksl4tNmNspjYM0OQRb1zbt5/OEdDtr3nRxzIvT9JrdyfKWb/ni/Dg+rnUsM75RqZT1R5jJ8/Lw7r53ydqs012eFsGqj7REW1wR65uDAAZoCCdDOC8gjF4zghCewe8f/GxR8kABAAA=