from os import path
import json
import monero_usd_price
import time
import logging
from src.thread_manager import ThreadManager
from src.subscription import Subscription

class Subscriptions():
    SUBS_FILE_PATH = 'Subscriptions.json'
    def __init__(self):
        self._subscriptions = self.read_subscriptions()
        self.logger = logging.getLogger(self.__module__)

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
                wait_seconds = 60
                for i in range(wait_seconds):

                    self.send_subscriptions()

                    self.logger.info('Checking subscriptions again in 1 min')
                    if ThreadManager.stop_flag().is_set():
                        break
                    time.sleep(wait_seconds)

            except Exception as e:
                self.logger.exception(e)

    def send_subscriptions(self):
        subscriptions = self.all()

        self.logger.info('Checking if subscriptions need to be paid.')

        for sub in subscriptions:
            sub.make_payment()
