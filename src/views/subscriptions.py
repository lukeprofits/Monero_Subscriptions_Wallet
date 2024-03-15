import customtkinter as ctk
from src.interfaces.view import View
import config as cfg
import subscription_functions

# View - NOT USED CURRENTLY
class SubscriptionsView(View):
    def build(self):
        return self


# Pop-up window
class Subscriptions(ctk.CTkToplevel):
    # Update subscriptions in config
    subscription_functions.get_subscriptions_from_file()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(cfg.SUBSCRIPTIONS_VIEW_GEOMETRY)

        #'''  # Comment out to make NOT fullscreen.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # '''

        self.my_frame = SubscriptionsScrollableFrame(master=self, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, sticky="nsew")


class SubscriptionsScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        title = ctk.CTkLabel(self, text=" My Subscriptions:", font=("Helvetica", 20))
        title.pack(padx=10, pady=(20, 0))

        # TODO: Would be cool to have a little section for "Assuming no price fluctuations, your wallet has enough funds to cover your subscription costs until X date."
        # TODO: There is probably a better way to word this, and we may want to assume a 20% price drop or something to be safe.

        separator = ctk.CTkFrame(self, height=2)
        separator.pack(fill='x', padx=10, pady=20)

        if cfg.subscriptions:
            for i, sub in enumerate(cfg.subscriptions):
                subscription_name = ctk.CTkLabel(self, text=f'{sub["custom_label"]}')
                subscription_name.pack(pady=0)

                subscription_price = ctk.CTkLabel(self, text=f'{sub["amount"]} {sub["currency"]}')
                subscription_price.pack()

                # TODO: Make this accurate. Right now it just shows billing cycle
                subscription_renews_in = ctk.CTkLabel(self, text=f'Renews In {sub["days_per_billing_cycle"]} Days')
                subscription_renews_in.pack()

                subscription_cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_subscription)
                subscription_cancel_button.pack(pady=(15, 30))

                # Separator
                separator = ctk.CTkFrame(self, height=2)  # bg_color="#ffffff" if needed

                # Do not pack separator if it's the last subscription
                if i < len(cfg.subscriptions) - 1:
                    separator.pack(fill='x', padx=10, pady=(0, 30))

        else:
            no_subs_text = ctk.CTkLabel(self, text="You haven't added any subscriptions.", )
            no_subs_text.pack(padx=10, pady=(20, 0))

            # TODO: Have this close the window, open "Pay".
            subscription_cancel_button = ctk.CTkButton(self, text="Add Subscription", command=self.cancel_subscription)
            subscription_cancel_button.pack(pady=10)

            separator = ctk.CTkFrame(self, height=2)
            separator.pack(fill='x', padx=10, pady=20)

    # TODO: Make this do something.
    def cancel_subscription(self):
            pass

    def open_main(self):
        self.master.master.master.switch_view('main') #TODO: Change this to something actually sane.

    def _create_subscription(self, sub):
        subscription_name = ctk.CTkLabel(self, text=sub["custom_label"])
        subscription_name.pack()

        subscription_price = ctk.CTkLabel(self, text=f"{sub['amount']} {sub['currency']}")
        subscription_price.pack()

        # TODO: Make this accurate. Right now it just shows billing cycle
        subscription_renews_in = ctk.CTkLabel(self, text=f"Renews In {sub['days_per_billing_cycle']} Days")
        subscription_renews_in.pack()

        subscription_cancel_button = ctk.CTkButton(self, text="Cancel", command=self.cancel_subscription)
        subscription_cancel_button.pack(pady=10)
