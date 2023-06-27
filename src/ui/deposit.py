from kivy.uix.gridlayout import GridLayout
from kivy.core.clipboard import Clipboard
from src.wallet import Wallet

class Deposit(GridLayout):
    def __init__(self, **kwargs):
        super(Deposit, self).__init__(**kwargs)

    def copy_address(self):
        Clipboard.copy(Wallet().address())