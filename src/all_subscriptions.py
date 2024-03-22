"""
A class that holds ALL Subcription objects
"""

import json
from os import path
from src.subscription import Subscription
import config as cfg


class AllSubscriptions:
    def __init__(self):
        self._subscriptions = self._read_file()

    def all(self):
        return self._subscriptions

    def _read_file(self):
        if not self._file_exists():
            self._write_file()

        with open(cfg.subs_file_path, "r") as file:
            raw_subscriptions = json.load(file)

        subscriptions = [Subscription(**sub) for sub in raw_subscriptions]

        # Sort subscriptions by billing_cycle_days
        subscriptions.sort(key=lambda x: x.days_per_billing_cycle)

        return subscriptions

    def _write_file(self):
        if not self._file_exists():
            self._subscriptions = []

        with open(cfg.subs_file_path, 'w') as file:
            prepared_subscriptions = [sub.json_friendly() for sub in self.all()]
            file.write(json.dumps(prepared_subscriptions, indent=4))

    def _set(self, subscriptions):
        self._subscriptions = subscriptions

    def _add(self, subscription):
        self._subscriptions.append(subscription)

    def _remove(self, subscription):
        self._subscriptions = [sub for sub in self._subscriptions if sub.json_friendly() != subscription.json_friendly()]
        return self._subscriptions

    def _file_exists(self):
        return path.exists(cfg.subs_file_path)

    def add(self, subscription):
        self._add(subscription)
        self._write_file()

    def remove(self, subscription):
        self._remove(subscription)
        self._write_file()