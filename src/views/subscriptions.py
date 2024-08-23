import customtkinter as ctk
from src.interfaces.view import View
import config as cfg
import styles
import json
from PIL import Image
from src.subscription import Subscription


class SubscriptionsView(View):
    def build(self):
        if len(json.loads(cfg.subscriptions())) > 1:
            self._app.geometry(styles.SUBSCRIPTIONS_LARGE_VIEW_GEOMETRY)
        else:
            self._app.geometry(styles.SUBSCRIPTIONS_SMALL_VIEW_GEOMETRY)

        # Back button and title
        styles.back_and_title(self, ctk, cfg, title='Manage Subscriptions:', pad_bottom=20)

        # Plus Button
        add_image = ctk.CTkImage(Image.open(styles.plus_icon), size=(24, 24))
        add_button = self.add(ctk.CTkButton(self._app, image=add_image, text='', fg_color='transparent', width=35, height=30, corner_radius=7, command=self.add_subscription))
        add_button.grid(row=0, column=2, padx=10, pady=(10, 20), sticky="e")

        # TODO: Would be cool to have a little section for "Assuming no price fluctuations, your wallet has enough funds to cover your subscription costs until X date."
        # TODO: There is probably a better way to word this, and we may want to assume a 20% price drop or something to be safe.

        self._app.grid_rowconfigure(1, weight=1)  # Changes this globally. Set back when closing view.

        self.my_frame = self.add(SubscriptionsScrollableFrame(master=self._app, corner_radius=0, fg_color="transparent"))

        return self

    def open_main(self):
        self._app.switch_view('main')

    def add_subscription(self):
        self._app.switch_view('pay')
        # self.master.master.master.switch_view('pay')

    def destroy(self):
        self._app.grid_rowconfigure(1, weight=0)
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
            no_subs_text = ctk.CTkLabel(self, text="     You haven't added any subscriptions yet.", )
            no_subs_text.pack(padx=10, pady=(50, 0))

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

       # Truncated to 50 characters
        self.subscription_name = ctk.CTkLabel(self, text=f'{sub.custom_label[:50]}:', font=styles.SUBHEADING_FONT_SIZE)
        self.subscription_name.grid(row=0, column=1, pady=0, sticky="ns")

        self.subscription_price = ctk.CTkLabel(self, text=f'{sub.amount} {sub.currency}', font=styles.SUBHEADING_FONT_SIZE)
        self.subscription_price.grid(row=1, column=1, pady=0,  sticky="ns")

        # TODO: Make this accurate. Right now it just shows billing cycle
        self.subscription_renews_in = ctk.CTkLabel(self, text=f'Renews In {sub.days_per_billing_cycle} Days', font=styles.BODY_FONT_SIZE)
        self.subscription_renews_in.grid(row=2, column=1, pady=0, sticky="ns")

        self.subscription_cancel_button = ctk.CTkButton(self, text="Cancel", corner_radius=15, command=lambda: self.cancel_subscription(sub))
        self.subscription_cancel_button.grid(row=3, column=1, pady=(10, 20))

        # Center the widgets within each column
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)  # Higher weight for the middle column
        self.columnconfigure(2, weight=1)

    def cancel_subscription(self, subscription):
        # cfg.config_file.remove_subscription(subscription)
        # self.destroy()
        cfg.SELECTED_SUBSCRIPTION = subscription
        self.master.master.master.master.switch_view('review_delete')
