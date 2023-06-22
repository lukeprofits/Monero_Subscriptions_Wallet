from kivy.uix.gridlayout import GridLayout
from src.wallet import Wallet
from kivy.properties import StringProperty

class Balance(GridLayout):
    dollar_balance = StringProperty('')
    xmr_balance = StringProperty('')

    def update_balance(self):
        balances = Wallet().balance()
        self.dollar_balance = balances[0]
        self.xmr_balance = balances[1]

    def __init__(self, **kwargs):
        super(Balance, self).__init__(**kwargs)
        self.update_balance()

    def on_dollar_balance(self, instance, text):
        print(f'{instance}:{text}')