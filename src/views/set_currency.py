import customtkinter as ctk
from src.interfaces.view import View

import config as cfg


class SetCurrencyView(View):
    def build(self):
        self._app.geometry(cfg.SET_CURRENCY_VIEW_GEOMETRY)

        def default_currency_selector_callback(choice):
            print(cfg.DEFAULT_CURRENCY)
            cfg.DEFAULT_CURRENCY = choice
            print("User chose:", choice)
            print("Now set to:", cfg.DEFAULT_CURRENCY)

        def secondary_currency_selector_callback(choice):
            print(cfg.SECONDARY_CURRENCY)
            print("User chose:", choice)
            cfg.SECONDARY_CURRENCY = choice
            print("Now set to:", cfg.SECONDARY_CURRENCY)

        SET_CURRENCY_TEXT = """Select the currencies that you would like for your wallet balance to be displayed in. 

                Primary will be shown by default. Click the amount shown to toggle to secondary."""

        # Title
        label = self.add(ctk.CTkLabel(self._app, text='Set Currencies:'))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Back Button
        back_button = self.add(ctk.CTkButton(self._app, text=cfg.BACK_BUTTON_EMOJI, font=(cfg.font, 24), width=35, height=30, command=self.open_main))
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        text = self.add(ctk.CTkLabel(self._app, text=SET_CURRENCY_TEXT))
        text.grid(row=1, column=0, columnspan=3, padx=20, pady=20, sticky="ew")

        # Labels
        label1 = self.add(ctk.CTkLabel(self._app, text='Default:'))
        label1.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        label2 = self.add(ctk.CTkLabel(self._app, text='Secondary:'))
        label2.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

        # TODO: Without selected_currency commented out, the buttons don't work on subsequest frames.
        # Default Currency
        selected_currency = ctk.StringVar(value=cfg.DEFAULT_CURRENCY)
        currency_selector = self.add(ctk.CTkOptionMenu(self._app, values=cfg.CURRENCY_OPTIONS, command=default_currency_selector_callback, variable=selected_currency))
        currency_selector.grid(row=3, column=0, columnspan=1, padx=20, pady=20)

        # Secondary Currency
        selected_currency = ctk.StringVar(value=cfg.SECONDARY_CURRENCY)
        currency_selector = self.add(ctk.CTkOptionMenu(self._app, values=cfg.CURRENCY_OPTIONS, command=secondary_currency_selector_callback, variable=selected_currency))
        currency_selector.grid(row=3, column=2, columnspan=1, padx=20, pady=20)

        return self

    def open_main(self):
        self._app.switch_view('main')


class SetCurrency(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry(cfg.SET_CURRENCY_VIEW_GEOMETRY)

        def default_currency_selector_callback(choice):
            print(cfg.DEFAULT_CURRENCY)
            cfg.DEFAULT_CURRENCY = choice
            print("User chose:", choice)
            print("Now set to:", cfg.DEFAULT_CURRENCY)

        def secondary_currency_selector_callback(choice):
            print(cfg.SECONDARY_CURRENCY)
            print("User chose:", choice)
            cfg.SECONDARY_CURRENCY = choice
            print("Now set to:", cfg.SECONDARY_CURRENCY)

        # Title
        label = ctk.CTkLabel(self, text='Set Currencies:')
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Back Button
        back_button = ctk.CTkButton(self, text=cfg.BACK_BUTTON_EMOJI, font=(cfg.font, 24), width=35, height=30, command=self.close)
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Labels
        label1 = ctk.CTkLabel(self, text='Default:')
        label1.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        label2 = ctk.CTkLabel(self, text='Secondary:')
        label2.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        # Default Currency
        selected_currency = ctk.StringVar(value=cfg.DEFAULT_CURRENCY)
        currency_selector = ctk.CTkOptionMenu(self, values=cfg.CURRENCY_OPTIONS, command=default_currency_selector_callback, variable=selected_currency)
        currency_selector.grid(row=2, column=0, columnspan=1, padx=20, pady=20)

        # Secondary Currency
        selected_currency = ctk.StringVar(value=cfg.SECONDARY_CURRENCY)
        currency_selector = ctk.CTkOptionMenu(self, values=cfg.CURRENCY_OPTIONS, command=secondary_currency_selector_callback, variable=selected_currency)
        currency_selector.grid(row=2, column=2, columnspan=1, padx=20, pady=20)

    def close(self):
        self.destroy()
