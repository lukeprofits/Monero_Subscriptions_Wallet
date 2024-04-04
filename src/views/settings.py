import customtkinter as ctk
from src.interfaces.view import View
import config as cfg
import src.views.set_currency as set_currency

class SettingsView(View):
    def __init__(self, app):
        super().__init__(app)
        self._app = app
        self.toplevel_window = None

    def build(self):
        self._app.geometry(cfg.SETTINGS_VIEW_GEOMETRY)
        # Configure the main window grid for spacing and alignment
        #self._app.columnconfigure([0, 1, 2], weight=1)  # 3 columns 2 rows

        BUTTONS_COL = 0
        BUTTONS_COL_SPAN = 3
        BUTTONS_PADX = 10
        BUTTONS_PADY = 5
        BUTTONS_STICKY = "ew"

        # Back button and title
        cfg.back_and_title(self, ctk, cfg, title=' Settings:')

        node_selection_button = self.add(ctk.CTkButton(self._app, text="Node Selection", command=self.open_node_selection))
        node_selection_button.grid(row=1, column=BUTTONS_COL, columnspan=BUTTONS_COL_SPAN, padx=BUTTONS_PADX, pady=(0, BUTTONS_PADY), sticky=BUTTONS_STICKY)

        welcome_message_button = self.add(ctk.CTkButton(self._app, text="Welcome Message", command=self.open_welcome_message))
        welcome_message_button.grid(row=2, column=BUTTONS_COL, columnspan=BUTTONS_COL_SPAN, padx=BUTTONS_PADX, pady=BUTTONS_PADY, sticky=BUTTONS_STICKY)

        manually_create_payment_request_button = self.add(ctk.CTkButton(self._app, text="Manually Create Monero Payment Request", command=self.open_manually_create_payment_request))
        manually_create_payment_request_button.grid(row=3, column=BUTTONS_COL, columnspan=BUTTONS_COL_SPAN, padx=BUTTONS_PADX, pady=BUTTONS_PADY, sticky=BUTTONS_STICKY)

        set_currency_button = self.add(ctk.CTkButton(self._app, text="Set Currency", command=self.open_set_currency))
        set_currency_button.grid(row=4, column=BUTTONS_COL, columnspan=BUTTONS_COL_SPAN, padx=BUTTONS_PADX, pady=BUTTONS_PADY, sticky=BUTTONS_STICKY)

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
        # Code for view (can't seem to get this working. It messes up any subsequest windows when closed)
        self._app.switch_view('set_currency')

        #''' # Code for pop-up window
        # if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
        #     self.toplevel_window = set_currency.SetCurrency(self._app)  # create window if its None or destroyed
        # else:
        #     self.toplevel_window.focus()  # if window exists focus it
        #'''
