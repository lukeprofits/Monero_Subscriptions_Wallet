from src.interfaces.observer import Observer
from src.exchange import Exchange
import config as cfg
from config import default_currency, secondary_currency

class BalanceObserver(Observer):
    def __init__(self, label):
        self.label = label

    def update(self, subject):
        if cfg.SHOW_DEFAULT_CURRENCY:
            balance = Exchange.display(to_sym=default_currency())
        else:
            balance = Exchange.display(to_sym=secondary_currency())
        self.label.configure(text=balance)
