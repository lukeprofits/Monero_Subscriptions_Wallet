from os import path
import json
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
            subscriptions = json.load(file)

        # Sort subscriptions by billing_cycle_days
        subscriptions.sort(key=lambda x: x['billing_cycle_days'])

        return subscriptions
