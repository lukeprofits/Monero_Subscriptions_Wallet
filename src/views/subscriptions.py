import customtkinter as ctk
from src.interfaces.view import View

import subscription_functions
import config as cfg


class SubscriptionsView(View):
    def __init__(self, app):
        self._app = app

    def build(self):
        # Update subscriptions in config
        subscription_functions.get_subscriptions_from_file()

        # TODO: Have @Probably_drunk review this. Frame does not fill window unless geometry width & height match my_frame width & height. Didn't used to be this way in the old version.
        width, height = 400, 600

        self._app.geometry(f"{str(width)}x{str(height)}")

        # Expand frame to fill window
        self._app.grid_rowconfigure(0, weight=1)
        self._app.grid_columnconfigure(0, weight=1)

        my_frame = self.add(SubscriptionsScrollableFrame(master=self._app, width=width, height=height, corner_radius=0, fg_color="transparent"))
        my_frame.grid(row=0, column=0, sticky="nsew")

        return self


class SubscriptionsScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.title = ctk.CTkLabel(self, text=" My Subscriptions:", font=(cfg.font, 20))
        self.title.pack(padx=10, pady=(20, 0))

        # TODO: Would be cool to have a little section for "Assuming no price fluctuations, your wallet has enough funds to cover your subscription costs until X date."
        # TODO: There is probably a better way to word this, and we may want to assume a 20% price drop or something to be safe.

        self.separator = ctk.CTkFrame(self, height=2)
        self.separator.pack(fill='x', padx=10, pady=20)

        if cfg.subscriptions:
            for sub in cfg.subscriptions:
                self.subscription_name = ctk.CTkLabel(self, text=f"{sub["custom_label"]}")
                self.subscription_name.pack()

                self.subscription_price = ctk.CTkLabel(self, text=f"{sub["amount"]} {sub["currency"]}")
                self.subscription_price.pack()

                # TODO: Make this accurate. Right now it just shows billing cycle
                self.subscription_renews_in = ctk.CTkLabel(self, text=f"Renews In {sub["days_per_billing_cycle"]} Days")
                self.subscription_renews_in.pack()

                self.subscription_cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_subscription)
                self.subscription_cancel_button.pack(pady=10)

                # Separator
                separator = ctk.CTkFrame(self, height=2)  # bg_color="#ffffff" if needed
                separator.pack(fill='x', padx=10, pady=20)
        else:
            self.no_subs_text = ctk.CTkLabel(self, text="You haven't added any subscriptions.", )
            self.no_subs_text.pack(padx=10, pady=(20, 0))

            # TODO: Have this close the window, open "Pay".
            self.subscription_cancel_button = ctk.CTkButton(self, text="Add Subscription", command=self.cancel_subscription)
            self.subscription_cancel_button.pack(pady=10)

            self.separator = ctk.CTkFrame(self, height=2)
            self.separator.pack(fill='x', padx=10, pady=20)


    # TODO: Make this do something.
    def cancel_subscription(self):
            pass