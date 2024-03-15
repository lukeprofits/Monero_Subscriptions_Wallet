import customtkinter as ctk
from src.interfaces.view import View
import config as cfg

class SettingsView(View):
    def build(self):
        self._app.geometry(cfg.SETTINGS_VIEW_GEOMETRY)
        # Configure the main window grid for spacing and alignment
        #self._app.columnconfigure([0, 1, 2], weight=1)  # 3 columns 2 rows

        BUTTONS_COL = 0
        BUTTONS_COL_SPAN = 3
        BUTTONS_PADX = 10
        BUTTONS_PADY = 5
        BUTTONS_STICKY = "ew"

        # Title
        label = self.add(ctk.CTkLabel(self._app, text=' Settings Window:'))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Back Button
        back_button = self.add(ctk.CTkButton(self._app, text=cfg.BACK_BUTTON_EMOJI, font=(cfg.font, 24), width=35, height=30, command=self.open_main))
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        node_selection_button = self.add(ctk.CTkButton(self._app, text="Node Selection", command=self.open_node_selection))
        node_selection_button.grid(row=1, column=BUTTONS_COL, columnspan=BUTTONS_COL_SPAN, padx=BUTTONS_PADX, pady=(0, BUTTONS_PADY), sticky=BUTTONS_STICKY)

        welcome_message_button = self.add(ctk.CTkButton(self._app, text="Welcome Message", command=self.open_welcome_message))
        welcome_message_button.grid(row=2, column=BUTTONS_COL, columnspan=BUTTONS_COL_SPAN, padx=BUTTONS_PADX, pady=BUTTONS_PADY, sticky=BUTTONS_STICKY)

        manually_create_payment_request_button = self.add(ctk.CTkButton(self._app, text="Manually Create Monero Payment Request", command=self.open_manually_create_payment_request))
        manually_create_payment_request_button.grid(row=3, column=BUTTONS_COL, columnspan=BUTTONS_COL_SPAN, padx=BUTTONS_PADX, pady=BUTTONS_PADY, sticky=BUTTONS_STICKY)

        set_currency_button = self.add(ctk.CTkButton(self._app, text="Set Currency", command=self.open_set_currency))
        set_currency_button.grid(row=4, column=BUTTONS_COL, columnspan=BUTTONS_COL_SPAN, padx=BUTTONS_PADX, pady=BUTTONS_PADY, sticky=BUTTONS_STICKY)

        # delete below if not needed 8-27-2024
        #toplevel_window = None

        return self

    def open_main(self):
        self._app.switch_view('main')

    def open_node_selection(self):
        self._app.switch_view('node_selection')

    def open_welcome_message(self):
        self._app.switch_view('welcome_message')

    def open_add_payment_request(self):
        self._app.switch_view('payment_request')

    def open_manually_create_payment_request(self):
        self._app.switch_view('manual_payment')

    # TODO: This does not exist yet and needs to be created.
    def open_set_currency(self):
        self._app.switch_view('set_currency')

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
