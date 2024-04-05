import customtkinter as ctk
from src.interfaces.view import View
import config as cfg


class AmountView(View):
    def build(self):
        def default_currency_selector_callback(choice):
            cfg.DEFAULT_CURRENCY = choice

            cfg.config_file.set(section='DEFAULT', option='default_currency', value=choice)
            cfg.config_file.write()
            #print("User chose:", choice)

        self._app.geometry(cfg.AMOUNT_VIEW_GEOMETRY)

        # Back button and title
        cfg.back_and_title(self, ctk, cfg, title='How Much:')

        # Frame to hold buttons
        center_frame = self.add(ctk.CTkFrame(self._app, ))
        center_frame.grid(row=1, column=0, columnspan=3, padx=0, pady=15, sticky="nsew")
        center_frame.columnconfigure([0, 1, 2, 3, 4, 5], weight=1)  # Frame will span 3 columns but contain two columns (0 and 1)

        # Input box
        self.input_box_for_amount = self.add(ctk.CTkEntry(center_frame, placeholder_text="Enter an amount"))
        self.input_box_for_amount.grid(row=0, column=2, padx=(10, 5), pady=0, sticky="ew")

        # TODO: Currently this is a visual and nothing else. Review!
        # Currency Selector
        selected_currency = ctk.StringVar(value=cfg.DEFAULT_CURRENCY)
        currency_selector = self.add(ctk.CTkOptionMenu(center_frame, values=cfg.CURRENCY_OPTIONS, command=default_currency_selector_callback,variable=selected_currency))
        currency_selector.grid(row=0, column=3, padx=(5, 10), pady=0, sticky="ew")


        # Wallet
        wallet = self.add(ctk.CTkLabel(self._app, text=f'To Wallet: {cfg.SEND_TO_WALLET[:5]}...{cfg.SEND_TO_WALLET[-5:]}'))  # TODO: Make it so that they can click the wallet to go back to "pay" view
        wallet.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Send button
        send_button = self.add(ctk.CTkButton(self._app, text="Send", command=self.send_button))
        send_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def send_button(self):
        # Send function
        wallet = cfg.SEND_TO_WALLET
        amount = self.input_box_for_amount.get().strip()
        self._app.switch_view('main')
