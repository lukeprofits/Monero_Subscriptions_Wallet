from os import path
import json
import monero_usd_price
import time
from src.wallet import Wallet
from src.thread_manager import ThreadManager
from src.subscription import Subscription

class Subscriptions():
    SUBS_FILE_PATH = 'Subscriptions.json'
    def __init__(self):
        self._subscriptions = self.read_subscriptions()

    def all(self):
        return self._subscriptions


    def read_subscriptions(self):
        if not path.exists(self.SUBS_FILE_PATH):
            return []

        with open(self.SUBS_FILE_PATH, "r") as file:
            raw_subscriptions = json.load(file)

        subscriptions = [Subscription(**sub) for sub in raw_subscriptions]

        # breakpoint()

        # Sort subscriptions by billing_cycle_days
        subscriptions.sort(key=lambda x: x.billing_cycle_days)

        return subscriptions

    def write_subscriptions(self):
        if not path.exists(self.SUBS_FILE_PATH):
            return []

        with open(self.SUBS_FILE_PATH, 'w') as file:
            prepared_subscriptions = [sub.json_friendly() for sub in self.all()]
            file.write(json.dumps(prepared_subscriptions))

    def set_subscriptions(self, subscriptions):
        self._subscriptions = subscriptions

    def add_subscription(self, subscription):
        self._subscriptions.append(subscription)

    def find_index(self, custom_label, amount, billing_cycle_days):
        for index, subscription in enumerate(self.all()):
            if (subscription.custom_label == custom_label and
                subscription.amount == amount and
                subscription.billing_cycle_days == billing_cycle_days):
                return index
        return None

    def find_subscription(self, custom_label, amount, billing_cycle_days):
        for index, subscription in enumerate(self.all()):
            if (subscription.custom_label == custom_label and
                subscription.amount == amount and
                subscription.billing_cycle_days == billing_cycle_days):
                return subscription
        return None

    def remove_subscription(self, subscription):
        self._subscriptions.remove(subscription)
        return self._subscriptions

    def send_recurring_payments(self):
        while not ThreadManager.stop_flag().is_set():
            try:
                subscriptions = self.all()

                print('Checking if subscriptions need to be paid.')

                for sub in subscriptions:
                    payment_is_due, payment_date = sub.determine_if_a_payment_is_due()

                    if payment_is_due:
                        sellers_wallet = sub.sellers_wallet
                        currency = sub.currency
                        amount = sub.amount
                        payment_id = sub.payment_id
                        wallet = Wallet()
                        if currency == 'USD':
                            print('SENDING USD')
                            xmr_amount = self.monero_from_usd(usd_amount=amount)
                            print(f'Sending {xmr_amount} XMR to {sellers_wallet} with payment ID {payment_id}')
                            wallet.send_subscription(sub)

                        elif currency == 'XMR':
                            print('SENDING XMR')
                            print(f'Sending {amount} XMR to {sellers_wallet} with payment ID {payment_id}')
                            wallet.send_subscription(sub)

                print('Checking subscriptions again in 1 min')
                for i in range(60):
                    if ThreadManager.stop_flag().is_set():
                        break
                    time.sleep(1)

            except Exception as e:
                print(f'Error in send_recurring_payments: {e}')

    def monero_from_usd(self, usd_amount, print_price_to_console=False):
        monero_price = monero_usd_price.median_price_not_threaded(print_price_to_console=print_price_to_console)
        monero_amount = round(usd_amount / monero_price, 12)
        if print_price_to_console:
            print(monero_amount)
        return monero_amount
