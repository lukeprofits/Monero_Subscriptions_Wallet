import customtkinter as ctk
from src.interfaces.view import View
from src.subscriptions import Subscriptions
import subscription_functions
import config as cfg


class SubscriptionsView(View):
    # Update subscriptions in config
    subscription_functions.get_subscriptions_from_file()

    def build(self):
        self._app.geometry(cfg.SUBSCRIPTIONS_VIEW_GEOMETRY)

        # Title
        title = self.add(ctk.CTkLabel(self._app, text=' My Subscriptions:'))
        title.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Back Button
        back_button = self.add(ctk.CTkButton(self._app, text=cfg.BACK_BUTTON_EMOJI, font=(cfg.font, 24), width=35, height=30, command=self.open_main))
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self._app.grid_rowconfigure(1, weight=1)

        self.my_frame = self.add(SubscriptionsScrollableFrame(master=self._app, corner_radius=0, fg_color="transparent"))
        self.my_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def destroy(self):
        self.my_frame._parent_frame.destroy()
        super().destroy()


class SubscriptionsScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.subscriptions = Subscriptions()

        # TODO: Would be cool to have a little section for "Assuming no price fluctuations, your wallet has enough funds to cover your subscription costs until X date."
        # TODO: There is probably a better way to word this, and we may want to assume a 20% price drop or something to be safe.

        separator = ctk.CTkFrame(self, height=2)
        separator.pack(fill='x', padx=10, pady=20)

        if self.subscriptions.all():
            i = 0
            for sub in self.subscriptions.all():
                subscription_name = ctk.CTkLabel(self, text=f'{sub.custom_label}')
                subscription_name.pack(pady=0)

                subscription_price = ctk.CTkLabel(self, text=f'{sub.amount} {sub.currency}')
                subscription_price.pack()

                # TODO: Make this accurate. Right now it just shows billing cycle
                subscription_renews_in = ctk.CTkLabel(self, text=f'Renews In {sub.days_per_billing_cycle} Days')
                subscription_renews_in.pack()

                subscription_cancel_button = ctk.CTkButton(self, text="Cancel", command=lambda: self.cancel_subscription(sub))
                subscription_cancel_button.pack(pady=(15, 30))

                # Separator
                separator = ctk.CTkFrame(self, height=2)  # bg_color="#ffffff" if needed

                # Do not pack separator if it's the last subscription
                if i < len(self.subscriptions.all()) - 1:
                    separator.pack(fill='x', padx=10, pady=(0, 30))
                i += 1

        else:
            no_subs_text = ctk.CTkLabel(self, text="You haven't added any subscriptions.", )
            no_subs_text.pack(padx=10, pady=(20, 0))

            # TODO: Have this close the window
            subscription_cancel_button = ctk.CTkButton(self, text="Add Subscription", command=self.add_subscription)
            subscription_cancel_button.pack(pady=10)

            separator = ctk.CTkFrame(self, height=2)
            separator.pack(fill='x', padx=10, pady=20)

    def cancel_subscription(self, subscription):
        #TODO: Make it remove the element from the list in the UI
        self.subscriptions.remove(subscription)

    def add_subscription(self):
        self.master.master.master.switch_view('pay')

    def open_main(self):
        self.master.master.master.switch_view('main')

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


'''
# Pop-up window - NOT USED CURRENTLY
class Subscriptions(ctk.CTkToplevel):
    # Update subscriptions in config
    subscription_functions.get_subscriptions_from_file()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(cfg.SUBSCRIPTIONS_VIEW_GEOMETRY)

        # Comment out to make NOT fullscreen.
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.my_frame = SubscriptionsScrollableFrame(master=self, corner_radius=0, fg_color="transparent")
        self.my_frame.grid(row=0, column=0, sticky="nsew")
'''