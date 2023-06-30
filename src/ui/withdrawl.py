from kivy.uix.gridlayout import GridLayout
from src.utils import valid_address
from src.wallet import Wallet

class Withdrawl(GridLayout):
    def __init__(self, **kwargs):
        super(Withdrawl, self).__init__(**kwargs)
        self.wallet = Wallet()

    def perform(self):
        if not self.wallet.send(self.ids.address, self.ids.amount):
            if not valid_address(self.ids.address):
                self.ids.address.background_color = CommonTheme().monero_orange
