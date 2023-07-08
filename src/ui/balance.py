from kivy.uix.gridlayout import GridLayout
from src.wallet import Wallet
from kivy.properties import StringProperty
from kivy.clock import Clock

class Balance(GridLayout):
    dollar_balance = StringProperty('')
    xmr_balance = StringProperty('')

    def update_balance(self, dt=None):
        if self.wallet.rpc_client.local_healthcheck():
            balances = self.wallet.balance()
            self.xmr_balance = str(balances[0])
            self.dollar_balance = str(balances[1])

    def __init__(self, **kwargs):
        super(Balance, self).__init__(**kwargs)
        self.wallet = Wallet()
        self.update_balance()
        Clock.schedule_interval(self.update_balance, 5)
