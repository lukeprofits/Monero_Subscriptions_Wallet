from kivy.uix.gridlayout import GridLayout
from src.utils import valid_address
from src.wallet import Wallet
from src.ui.common import CommonTheme

class Withdrawl(GridLayout):
    def __init__(self, **kwargs):
        super(Withdrawl, self).__init__(**kwargs)
        self.wallet = Wallet()

    def perform(self):
        destination_address = self.ids.destination_address.text
        if not valid_address(destination_address):
            self.ids.destination_address.background_color = CommonTheme().monero_orange

        amount = self.ids.amount.text
        if not amount:
            self.ids.amount.background_color = CommonTheme().monero_orange

        if not valid_address(destination_address) or not amount:
            return False

        self.wallet.send(destination_address, amount)
