import customtkinter as ctk
from src.interfaces.view import View


class SettingsView(View):
    def __init__(self, app):
        self._app = app

    def build(self):

        self._app.geometry("400x600")

        label = self.add(ctk.CTkLabel(self._app, text="Settings Window"))
        label.pack(padx=20, pady=20)

        node_selection_button = self.add(ctk.CTkButton(self._app, text="Node Selection", command=self.open_node_selection))
        node_selection_button.pack(side="top", padx=20, pady=20)

        welcome_message_button = self.add(ctk.CTkButton(self._app, text="Welcome Message", command=self.open_welcome_message))
        welcome_message_button.pack(side="top", padx=20, pady=20)

        manually_create_payment_request_button = self.add(ctk.CTkButton(self._app, text="Manually Create Monero Payment Request", command=self.open_manually_create_payment_request))
        manually_create_payment_request_button.pack(side="top", padx=20, pady=20)

        set_currency_button = self.add(ctk.CTkButton(self._app, text="Set Currency", command=self.open_set_currency))
        set_currency_button.pack(side="top", padx=20, pady=20)

        toplevel_window = None

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
