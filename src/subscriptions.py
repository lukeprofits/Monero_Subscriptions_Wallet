import json
from os import path
from src.subscription import Subscription

class Subscriptions():
    SUBS_FILE_PATH = 'Subscriptions.json'

    def __init__(self):
        self._subscriptions = []
        self._write_file()
        self._subscriptions = self._read_file()

    def all(self):
        return self._subscriptions

    def _read_file(self):
        if not self._file_exists():
            return []

        with open(self.SUBS_FILE_PATH, "r") as file:
            raw_subscriptions = json.load(file)

        subscriptions = [Subscription(**sub) for sub in raw_subscriptions]

        # Sort subscriptions by billing_cycle_days
        subscriptions.sort(key=lambda x: x.billing_cycle_days)

        return subscriptions

    def _write_file(self):
        if not self._file_exists():
            return []

        with open(self.SUBS_FILE_PATH, 'w') as file:
            prepared_subscriptions = [sub.json_friendly() for sub in self.all()]
            file.write(json.dumps(prepared_subscriptions))

    def _set(self, subscriptions):
        self._subscriptions = subscriptions

    def _add(self, subscription):
        self._subscriptions.append(subscription)

    def _remove(self, subscription):
        self._subscriptions.remove(subscription)
        return self._subscriptions

    def _file_exists(self):
        return path.exists(self.SUBS_FILE_PATH)

    def add(self, subscription):
        self._add(subscription)
        self._write_file()