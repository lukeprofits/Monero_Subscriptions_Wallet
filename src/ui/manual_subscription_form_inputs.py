from kivy.uix.gridlayout  import GridLayout
from src.ui.currency import CurrencyDropdown, CurrencyButton
from src.ui.common import CommonTheme

class ManualSubscriptionFormInputs(GridLayout):
    def on_kv_post(self, idk):
        self.currency_dropdown = CurrencyDropdown()
        self.currency_button = CurrencyButton(text="Currency")
        self.add_widget(self.currency_button)
        self.ids['currency'] = self.currency_button
        self.currency_button.bind(on_release=self.button_callback)

        self.currency_dropdown.bind(on_select = lambda instance, x: setattr(self.currency_button, 'text', x))
        self.currency_dropdown.bind(on_select = self.callback)

    def button_callback(self, idk):
        # breakpoint()
        self.currency_dropdown.open(idk)
        self.currency_button.background_color = CommonTheme().monero_white

    def callback(self, instance, x):
        '''x is self.mainbutton.text refreshed'''
        print ( "The chosen mode is: {0}" . format ( x ) )
