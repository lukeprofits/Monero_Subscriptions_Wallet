import customtkinter as ctk

import styles
from src.interfaces.view import View
from src.exchange import Exchange
import config as cfg
from config import default_currency, secondary_currency

class SetCurrencyView(View):
    def build(self):
        self._app.geometry(styles.SET_CURRENCY_VIEW_GEOMETRY)

        def default_currency_selector_callback(choice):
            cfg.config_file.set(section='subscriptions', option='default_currency', value=choice)
            cfg.config_file.write()
            #print("User chose:", choice)

        def secondary_currency_selector_callback(choice):
            cfg.config_file.set(section='subscriptions', option='secondary_currency', value=choice)
            cfg.config_file.write()
            # print("User chose:", choice)

        # Back button and title
        styles.back_and_title(self, ctk, cfg, title=' Set Currencies:')

        # Labels
        label1 = self.add(ctk.CTkLabel(self._app, text='Default:'))
        label1.grid(row=2, column=0, padx=10, pady=(15, 5), sticky="ew")

        label2 = self.add(ctk.CTkLabel(self._app, text='Secondary:'))
        label2.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

        # TODO: Without selected_currency commented out, the buttons don't work on subsequest frames.
        # Default Currency
        selected_currency = ctk.StringVar(value=default_currency())
        currency_selector = self.add(ctk.CTkOptionMenu(self._app, values=Exchange.options(), corner_radius=15, command=default_currency_selector_callback, variable=selected_currency))
        currency_selector.grid(row=3, column=0, columnspan=1, padx=20, pady=(5, 35))

        # Secondary Currency
        selected_currency = ctk.StringVar(value=secondary_currency())
        currency_selector = self.add(ctk.CTkOptionMenu(self._app, values=Exchange.options(), corner_radius=15, command=secondary_currency_selector_callback, variable=selected_currency))
        currency_selector.grid(row=3, column=2, columnspan=1, padx=20, pady=(5, 35))

        return self

    def open_main(self):
        self._app.switch_view('main')
