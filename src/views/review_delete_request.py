import customtkinter as ctk
import monero_usd_price
from src.interfaces.view import View
from src.subscription import Subscription
import config as cfg
import clipboard
import monerorequest
from datetime import datetime


class ReviewDeleteRequestView(View):
    def build(self):
        self._app.geometry(cfg.SUBSCRIPTIONS_VIEW_NO_SUBS_GEOMETRY)

        # Title
        label = self.add(ctk.CTkLabel(self._app, text='Cancel Subscription?', font=cfg.HEADINGS_FONT_SIZE))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=(50, 5), sticky="ew")

        # Frame to hold buttons
        center_frame = self.add(ctk.CTkFrame(self._app, ))
        center_frame.grid(row=1, column=0, columnspan=3, padx=0, pady=15, sticky="nsew")
        center_frame.columnconfigure([0, 1, 2, 3, 4, 5], weight=1)  # Frame will span 3 columns but contain two columns (0 and 1)

        # No Button
        no_button = self.add(ctk.CTkButton(center_frame, text="No", command=self.open_main))
        no_button.grid(row=0, column=2, padx=(10, 5), pady=0, sticky="ew")

        # Yes Button
        yes_button = self.add(ctk.CTkButton(center_frame, text="Yes", command=self.cancel_action))
        yes_button.grid(row=0, column=3, padx=(5, 10), pady=0, sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('subscriptions')

    def cancel_action(self):
        cfg.config_file.remove_subscription(cfg.SELECTED_SUBSCRIPTION)
        cfg.SELECTED_SUBSCRIPTION = ''
        self._app.switch_view('subscriptions')
