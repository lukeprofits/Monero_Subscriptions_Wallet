import customtkinter as ctk
from src.interfaces.view import View

import config as cfg

class SetCurrencyView(View):
    def __init__(self, app):
        self._app = app

    def build(self):
        self._app.geometry(cfg.RECEIVE_VIEW_GEOMETRY)

        # Title
        label = self.add(ctk.CTkLabel(self._app, text=' Set Currency:'))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Back Button
        back_button = self.add(ctk.CTkButton(self._app, text=cfg.BACK_BUTTON_EMOJI, font=(cfg.font, 24), width=35, height=30, command=self.open_main))
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Wallet input box
        # Documentation: https://customtkinter.tomschimansky.com/documentation/widgets/entry
        #input_box_for_wallet_or_request = self.add(ctk.CTkEntry(self._app, placeholder_text="Enter a monero payment request or wallet address..."))
        #input_box_for_wallet_or_request.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        copy_wallet_button = self.add(ctk.CTkButton(self._app, text="Copy Wallet Address", command=self.copy_wallet_address))
        copy_wallet_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def copy_wallet_address(self):
        self._app.switch_view('main')  # TODO: UPDATE THIS TO WORK!!!

    # This was the old code for that window
    '''
    class SetCurrency(ctk.CTkToplevel):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.geometry("600x300")

            def default_currency_selector_callback(choice):
                global DEFAULT_CURRENCY
                print(DEFAULT_CURRENCY)
                DEFAULT_CURRENCY = choice
                print("User chose:", choice)
                print("Now set to:", DEFAULT_CURRENCY)

            def secondary_currency_selector_callback(choice):
                global SECONDARY_CURRENCY
                print(SECONDARY_CURRENCY)
                print("User chose:", choice)
                SECONDARY_CURRENCY = choice
                print("Now set to:", SECONDARY_CURRENCY)

            set_currency_window_text = """
            Set Default Currency:

            The currency that you select will be shown by default. 

            To toggle to the the Monero amount in the main window, simply click it."""

            self.label = ctk.CTkLabel(self, text=set_currency_window_text)
            self.label.pack(padx=20, pady=20)

            # Default Currency
            self.selected_currency = ctk.StringVar(value=DEFAULT_CURRENCY)
            self.currency_selector = ctk.CTkOptionMenu(self, values=CURRENCY_OPTIONS, command=default_currency_selector_callback, variable=self.selected_currency)
            self.currency_selector.pack(padx=20, pady=20)

            # Secondary Currency
            self.selected_currency = ctk.StringVar(value=SECONDARY_CURRENCY)
            self.currency_selector = ctk.CTkOptionMenu(self, values=CURRENCY_OPTIONS, command=secondary_currency_selector_callback, variable=self.selected_currency)
            self.currency_selector.pack(padx=20, pady=20)    
    '''
