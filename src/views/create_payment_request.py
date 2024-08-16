import customtkinter as ctk
import tkinter
from tkcalendar import Calendar, DateEntry  # TODO: only some of this is used for calendar view

from datetime import datetime, timezone
from src.exchange import Exchange
from src.interfaces.view import View
from config import default_currency
import config as cfg
import styles
import clipboard
import monerorequest
from src.wallet import Wallet
import re


class CreatePaymentRequestView(View):
    def build(self):
        def on_date_click(event):
            # This function can be used to handle any additional actions when the date is clicked
            print("Date selected:", self.start_date_input.get())
            self.start_date_input.focus_force()

        def selected_currency_callback(choice):
            cfg.CURRENT_CREATE_PAYMENT_REQUEST_CURRENCY = choice

        self._app.geometry(styles.CREATE_PAYMENT_REQUEST_VIEW_GEOMETRY)

        # TODO: Can we set the border color through the theme file instead?
        # Border Color
        bc = styles.monero_orange
        x = 10  # 70
        y = 5  # (27.5, 20)

        heading_frame = self.add(ctk.CTkFrame(self._app))
        heading_frame.columnconfigure([0, 1, 2], weight=1)
        heading_frame.pack(fill='x', padx=0, pady=0)

        # Back Button
        back_image = ctk.CTkImage(styles.Image.open(styles.back_icon), size=(24, 24))
        back_button = self.add(ctk.CTkButton(heading_frame, image=back_image, text='', fg_color='transparent', width=35, height=30, corner_radius=7, command=self.open_main))
        back_button.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        # Title
        label = self.add(ctk.CTkLabel(heading_frame, text='Create Payment Request:', font=styles.HEADINGS_FONT_SIZE))
        label.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="ew")

        # TODO: Doing this to get it to display properly. There is probably a better way to do this.
        spacer = self.add(ctk.CTkLabel(heading_frame, text=''))
        spacer.grid(row=0, column=3, padx=10, pady=(10, 0), sticky="e")



        content_frame = self.add(ctk.CTkFrame(self._app))
        content_frame.pack(fill='both', expand=True, padx=0, pady=0)
        # Configure the grid layout to have 100 columns with equal size
        for i in range(10):
            content_frame.grid_columnconfigure(i, weight=1)

        # Input Title Section
        self.custom_label_input = self.add(ctk.CTkEntry(content_frame, placeholder_text="Title", corner_radius=15, border_color=bc))  # font=(styles.font, 12),
        self.custom_label_input.grid(row=0, column=0, columnspan=10, padx=x, pady=(10 + y, y), sticky="ew")

        # Pricing & Payments Section
        self.number_of_payments_input = self.add(ctk.CTkEntry(content_frame, placeholder_text="# Payments", corner_radius=15, border_color=bc))  # font=(styles.font, 12),
        payment_count_options = ["A Subscription", "1 Payment"]
        for i in range(366):
            if i > 1:
                payment_count_options.append(f"{i} Payments")
        selected_number_of_payments = ctk.StringVar(value=payment_count_options[0])
        self.number_of_payments_input = self.add(ctk.CTkOptionMenu(content_frame, values=payment_count_options, corner_radius=15,command=selected_currency_callback, variable=selected_number_of_payments))
        self.number_of_payments_input.grid(row=1, column=0, columnspan=4, padx=(x, (x / 2)), pady=y, sticky="ew")

        payments_of = self.add(ctk.CTkLabel(content_frame, text="of", font=styles.BODY_FONT_SIZE))
        payments_of.grid(row=1, column=4, columnspan=2, padx=(x / 2), pady=y, sticky="ew")

        self.amount_input = self.add(ctk.CTkEntry(content_frame, placeholder_text="Price", corner_radius=15, border_color=bc))  # font=(styles.font, 12),
        self.amount_input.grid(row=1, column=6, columnspan=2, padx=(x / 2), pady=y, sticky="ew")

        selected_currency = ctk.StringVar(value=default_currency())
        self.currency_input = self.add(ctk.CTkOptionMenu(content_frame, values=Exchange.options(), corner_radius=15, command=selected_currency_callback, variable=selected_currency))
        self.currency_input.grid(row=1, column=8, columnspan=2, padx=((x / 2), x), pady=y, sticky="ew")

        # Billing Frequency Section
        day_options = []
        for i in range(366):
            if i > 0:
                day_options.append(f"Bills every {i} days")
        selected_number_of_days = ctk.StringVar(value=day_options[29])
        self.days_per_billing_cycle = self.add(ctk.CTkOptionMenu(content_frame, values=day_options, corner_radius=15, command=selected_currency_callback, variable=selected_number_of_days))
        self.days_per_billing_cycle.grid(row=2, column=0, columnspan=7, padx=(x, (x / 2)), pady=y, sticky="ew")

        starting_on = self.add(ctk.CTkLabel(content_frame, text="starting on", font=styles.BODY_FONT_SIZE))
        starting_on.grid(row=2, column=7, columnspan=1, padx=(x / 2), pady=y, sticky="ew")

        # input field
        self.start_date_input = self.add(ctk.CTkEntry(content_frame, placeholder_text="mm/dd/yyyy", corner_radius=15, border_color=bc))
        self.start_date_input.grid(row=2, column=8, columnspan=2, padx=((x / 2), x), pady=y, sticky="ew")

        # Calendar
        #self.start_date_input = self.add(Calendar(content_frame))
        #self.start_date_input.grid(row=2, column=8, columnspan=2, padx=((x / 2), x), pady=y, sticky="ew")

        # Click open calendar
        #self.start_date_input = self.add(DateEntry(content_frame, width=12, background='darkblue', foreground='white', borderwidth=2))
        #self.start_date_input.grid(row=2, column=8, columnspan=2, padx=((x / 2), x), pady=y, sticky="ew")
        #self.start_date_input.bind("<Button-1>", on_date_click)

        # Sellers Wallet Section
        self.sellers_wallet_input = self.add(ctk.CTkEntry(content_frame, placeholder_text="Sellers Wallet", corner_radius=15, border_color=bc))  # font=(styles.font, 12),
        self.sellers_wallet_input.grid(row=3, column=0, columnspan=10, padx=x, pady=y, sticky="ew")


        # TODO: Make this a toggle in settings, but by default do not show optional settings
        '''
        # Optional Settings Section
        optional_text = self.add(ctk.CTkLabel(content_frame, text="Optional:", font=styles.SUBHEADING_FONT_SIZE))
        optional_text.grid(row=4, column=0, columnspan=10, padx=((x * 2), 5), pady=y, sticky="ew")


        
        self.change_indicator_url_input = self.add(ctk.CTkEntry(content_frame, placeholder_text="Change Indicator URL", corner_radius=15, border_color=bc))  #font=(styles.font, 12),
        self.change_indicator_url_input.grid(row=5, column=0, columnspan=8, padx=(x, 5), pady=(y, 5 + y), sticky="ew")

        self.payment_id_input = self.add(ctk.CTkEntry(content_frame, placeholder_text="Payment ID", corner_radius=15, border_color=bc))  # font=(styles.font, 12),
        self.payment_id_input.grid(row=5, column=8, columnspan=2, padx=(5, x), pady=(y, 5 + y), sticky="ew")
        #'''


        # Submit button
        create_button = self.add(ctk.CTkButton(content_frame, text="Create Payment Request", corner_radius=15, command=self.create_button))
        create_button.grid(row=6, column=0, columnspan=10, padx=120, pady=10, sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def create_button(self):
        # Pull in all info and process
        custom_label = self.custom_label_input.get().strip()
        print(custom_label, type(custom_label))

        sellers_wallet = self.sellers_wallet_input.get().strip()
        print(sellers_wallet, type(sellers_wallet))

        currency = self.currency_input.get().strip()
        print(currency, type(currency))

        amount = self.amount_input.get().strip()
        print(amount, type(amount))

        payment_id = monerorequest.make_random_payment_id()
        print(payment_id, type(payment_id))

        # TODO: FIX THIS TO USE THE TIME ENTERED AND SHOW DEFAULT TIME AS PLACEHOLDER
        start_date = self.start_date_input.get().strip() if self.start_date_input.get().strip() else datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        print(start_date, type(start_date))

        days_per_billing_cycle = int(re.sub(r'\D', '', self.days_per_billing_cycle.get().strip()))
        print(days_per_billing_cycle, type(days_per_billing_cycle))

        number_of_payments = int(re.sub(r'\D', '', self.number_of_payments_input.get().strip())) if re.sub(r'\D', '', self.number_of_payments_input.get().strip()) else 0
        print(number_of_payments, type(number_of_payments))

        change_indicator_url = ''
        print(change_indicator_url, type(change_indicator_url))

        version = '1'
        print(version, type(version))

        payment_request = monerorequest.make_monero_payment_request(
            custom_label=custom_label,
            sellers_wallet=sellers_wallet,
            currency=currency,
            amount=amount,
            payment_id=payment_id,
            start_date=start_date,
            days_per_billing_cycle=days_per_billing_cycle,
            number_of_payments=number_of_payments,
            change_indicator_url=change_indicator_url,
            version=version
        )

        clipboard.copy(payment_request)
        print(payment_request)
        self._app.switch_view('copy_payment_request')
