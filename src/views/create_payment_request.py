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


class CreatePaymentRequestView(View):
    def build(self):
        def selected_currency_callback(choice):
            cfg.CURRENT_CREATE_PAYMENT_REQUEST_CURRENCY = choice

        self._app.geometry(styles.CREATE_PAYMENT_REQUEST_VIEW_GEOMETRY)

        # Back button and title
        styles.back_and_title(self, ctk, cfg, title='Create Payment Request:')

        # TODO: Can we set the border color through the theme file instead?
        # Border Color
        bc = styles.monero_orange
        x = 70
        y = 5  #(27.5, 20)


        self.custom_label_input = self.add(ctk.CTkEntry(self._app, placeholder_text="What is it for?", corner_radius=15, border_color=bc))  #font=(styles.font, 12),
        self.custom_label_input.grid(row=1, column=0, columnspan=3, padx=x, pady=(10+y, y), sticky="ew")

        self.currency_input = self.add(ctk.CTkEntry(self._app, placeholder_text="Pricing based on what currency?", corner_radius=15, border_color=bc))  # font=(styles.font, 12),

        selected_currency = ctk.StringVar(value=default_currency())
        currency_input = self.add(ctk.CTkOptionMenu(self._app, values=Exchange.options(), corner_radius=15, command=selected_currency_callback, variable=selected_currency))
        currency_input.grid(row=2, column=0, padx=x, pady=y, sticky="ew")

        #self.currency_input.grid(row=2, column=0, columnspan=3, padx=x, pady=y, sticky="ew")

        self.amount_input = self.add(ctk.CTkEntry(self._app, placeholder_text="Price per billing cycle?", corner_radius=15, border_color=bc))  # font=(styles.font, 12),
        self.amount_input.grid(row=3, column=0, columnspan=3, padx=x, pady=y, sticky="ew")

        self.days_per_billing_cycle_input = self.add(ctk.CTkEntry(self._app, placeholder_text="Billing every _ days", corner_radius=15, border_color=bc))  # font=(styles.font, 12),
        self.days_per_billing_cycle_input.grid(row=4, column=0, columnspan=3, padx=x, pady=y, sticky="ew")

        self.start_date_input = self.add(ctk.CTkEntry(self._app, placeholder_text="Start Date? (mm/dd/yyyy)", corner_radius=15, border_color=bc))  #font=(styles.font, 12),
        self.start_date_input.grid(row=5, column=0, columnspan=3, padx=x, pady=y, sticky="ew")

        self.number_of_payments_input = self.add(ctk.CTkEntry(self._app, placeholder_text="Number of Payments (use 0 for until canceled)", corner_radius=15, border_color=bc))  #font=(styles.font, 12),
        self.number_of_payments_input.grid(row=6, column=0, columnspan=3, padx=x, pady=y, sticky="ew")

        # Consider having these as ADVANCED settings that you have to expand to see
        self.sellers_wallet_input = self.add(ctk.CTkEntry(self._app, placeholder_text="Sellers Wallet", corner_radius=15, border_color=bc))  # font=(styles.font, 12),
        self.sellers_wallet_input.grid(row=7, column=0, columnspan=3, padx=x, pady=y, sticky="ew")

        self.change_indicator_url_input = self.add(ctk.CTkEntry(self._app, placeholder_text="Change Indicator URL (Optional)", corner_radius=15, border_color=bc))  #font=(styles.font, 12),
        self.change_indicator_url_input.grid(row=8, column=0, columnspan=3, padx=x, pady=y, sticky="ew")

        self.payment_id_input = self.add(ctk.CTkEntry(self._app, placeholder_text="Payment ID (Optional)", corner_radius=15, border_color=bc))  # font=(styles.font, 12),
        self.payment_id_input.grid(row=9, column=0, columnspan=3, padx=x, pady=(y, 5 + y), sticky="ew")

        # Create button
        create_button = self.add(ctk.CTkButton(self._app, text="Create Payment Request", corner_radius=15, command=self.create_button))
        create_button.grid(row=10, column=0, columnspan=3, padx=120, pady=10, sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def create_button(self):
        self._app.switch_view('main')
