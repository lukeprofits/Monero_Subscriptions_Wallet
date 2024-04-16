"""
The "Manage Subscriptions" window
"""

import customtkinter as ctk
from src.interfaces.view import View
import config as cfg
import json
from src.subscription import Subscription

class SubscriptionsView(View):
    def build(self):
        # If we have existing subscriptions
        if len(json.loads(cfg.subscriptions())) > 1:
            self._app.geometry(cfg.SUBSCRIPTIONS_VIEW_GEOMETRY)
        # If we have no existing subscriptions
        else:
            self._app.geometry(cfg.SUBSCRIPTIONS_VIEW_NO_SUBS_GEOMETRY)

        # Back button and title
        cfg.back_and_title(self, ctk, cfg, title='Manage Subscriptions:')

        # TODO: Would be cool to have a little section for "Assuming no price fluctuations, your wallet has enough funds to cover your subscription costs until X date."
        # TODO: There is probably a better way to word this, and we may want to assume a 20% price drop or something to be safe.

        self._app.grid_rowconfigure(1, weight=1)

        self.my_frame = self.add(SubscriptionsScrollableFrame(master=self._app, corner_radius=0, fg_color="transparent"))

        return self

    def open_main(self):
        self._app.switch_view('main')

    def destroy(self):
        self.my_frame._parent_frame.destroy()
        super().destroy()


class SubscriptionsScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=1, column=0, columnspan=3, sticky='nsew')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        subscriptions = json.loads(cfg.subscriptions())

        if subscriptions:
            for i, sub in enumerate(subscriptions):
                self._create_subscription(Subscription(**sub), i)

        else:
            no_subs_text = ctk.CTkLabel(self, text="You haven't added any subscriptions.", )
            no_subs_text.pack(padx=10, pady=(20, 0))

            # TODO: Have this close the window
            subscription_cancel_button = ctk.CTkButton(self, text="Add Subscription", command=self.add_subscription)
            subscription_cancel_button.pack(pady=10)

            separator = ctk.CTkFrame(self, height=2)
            separator.pack(fill='x', padx=10, pady=20)

    def add_subscription(self):
        self.master.master.master.switch_view('pay')

    def open_main(self):
        self.master.master.master.switch_view('main')

    def _create_subscription(self, sub, row):
        SubscriptionFrame(self, sub, row)

class SubscriptionFrame(ctk.CTkFrame):
    def __init__(self, master, sub, row, **kwargs):
        super().__init__(master, **kwargs)

        # Padding and stuff for each SubscriptionFrame
        self.grid(row=row, column=1, columnspan=3, sticky="nsew", padx=10, pady=(0, 10))

        self.subscription_name = ctk.CTkLabel(self, text=f'{sub.custom_label}:', font=cfg.SUBHEADING_FONT_SIZE)
        self.subscription_name.grid(row=0, column=1, pady=0)

        self.subscription_price = ctk.CTkLabel(self, text=f'{sub.amount} {sub.currency}', font=cfg.SUBHEADING_FONT_SIZE)
        self.subscription_price.grid(row=1, column=1, pady=0)

        # TODO: Make this accurate. Right now it just shows billing cycle
        self.subscription_renews_in = ctk.CTkLabel(self, text=f'Renews In {sub.days_per_billing_cycle} Days', font=cfg.BODY_FONT_SIZE)
        self.subscription_renews_in.grid(row=2, column=1, pady=0)

        self.subscription_cancel_button = ctk.CTkButton(self, text="Cancel", command=lambda: self.cancel_subscription(sub))
        self.subscription_cancel_button.grid(row=3, column=1, pady=(10, 20))

        # Center the widgets within each column
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)  # Higher weight for the middle column
        self.columnconfigure(2, weight=1)

    def cancel_subscription(self, subscription):
        cfg.config_file.remove_subscription(subscription)
        #TODO: Display the "Add Subscription" Button when Subscriptions are empty
        self.destroy()
