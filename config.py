"""
Configuration File for Monero Subscriptions Wallet
Contains global settings and variables used across the application.

Using this for fiat currencies (other than the hard-coded ones): https://github.com/datasets/currency-codes

Exchange rates scraped from XE.com
"""

import os
import platform
import requests
from io import StringIO
import csv
import monero_usd_price
from lxml import html
from decimal import Decimal, ROUND_HALF_UP
import argparse
from configparser import ConfigParser
import re
import json
from src.subscription import Subscription

SHOULD_CENTER_WINDOW = True

NODE_URL = 'xmr-node.cakewallet.com:18081'

# This sets the defaults for config.ini when initially created. It does NOT overwrite an existing config.ini
config_options = {
    'rpc': {
        'rpc_bind_port': 18088,
        'rpc_username': 'monero',
        'rpc_password': 'monero',
        'rpc': True,
        'local_rpc_url': 'http://127.0.0.1:18088/json_rpc',
        'node_url': NODE_URL,
        'daemon_url': f'{NODE_URL}/json_rpc',
        'wallet_dir': 'wallets'
    },
    'subscriptions': {
        'subscriptions': [],
        'default_currency': 'USD',
        'secondary_currency': 'XMR'
    },
    'other': {
        'is_first_launch': True
    }

}

parser=argparse.ArgumentParser()
parser.add_argument('--rpc-bind-port', type=int)
parser.add_argument('--local-rpc-url')
parser.add_argument('--rpc-username')
parser.add_argument('--rpc-password')
parser.add_argument('--rpc', type=bool, action=argparse.BooleanOptionalAction)
parser.add_argument('--node-url')
parser.add_argument('--cli-path')
parser.add_argument('--daemon-url')
parser.add_argument('--config-file')
parser.add_argument('--wallet-dir')
parser.add_argument('--subscriptions')
parser.add_argument('--default-currency')
parser.add_argument('--secondary-currency')
parser.add_argument('--is-first-launch')
args=parser.parse_args()


class ConfigFile():
    def __init__(self, path='./config.ini'):
        self._config = ConfigParser()
        self._path = path
        self._observers = []

        if self.exists():
            self.read()
        else:
            self.create()

    def read(self):
        options = {}
        if self.exists():
            options = self._config.read(self._path)
        return options

    def write(self):
        with open(self._path, 'w') as conf:
            self._config.write(conf)

    def exists(self):
        return os.path.isfile(self._path)

    def set_defaults(self):
        for section, options in config_options.items():
            for option, value in options.items():
                self._config['DEFAULT'][option] = str(value)

    def set(self, section, option, value):
        self._config[section][option] = value

    def get(self, section, option):
        return self._config.get(section, option)

    def create(self):
        self.set_defaults()
        for section in config_options.keys():
            self._config[section] = {}
        self.write()

    def add_subscription(self, subscription):
        subs = json.loads(self.get('subscriptions', 'subscriptions'))
        subs.append(subscription.json_friendly())
        self.set('subscriptions', 'subscriptions', json.dumps(subs))
        self.write()
        return True

    def remove_subscription(self, subscription):
        subs = [sub for sub in json.loads(self.get('subscriptions', 'subscriptions')) if sub != subscription.json_friendly()]
        self.set('subscriptions', 'subscriptions', json.dumps(subs))
        self.write()
        return True

config_file = ConfigFile(args.config_file or './config.ini')

def variable_value(args, section, option):
    # Get From CLI Options
    value = getattr(args, option)

    # Get From Config File
    if value is None:
        value = config_file.get(section, option)

    # Get From Environment
    if value is None:
        value = os.environ.get(option.upper())

    # Get Default Value
    if value is None:
        value = config_options[section][option]

    return value


# Set CLI Options as importable variables
for section, options in config_options.items():
    for option in options.keys():
        exec(f'{option} = lambda: variable_value(args, "{section}", "{option}")')


# =====================
# Placeholders and Dynamic Values
# =====================
xmr_unlocked_balance = '--.------------'
wallet_balance_xmr = '--.------------'
wallet_balance_usd = '---.--'
current_monero_price = 150.00
wallet_address = ''


def get_platform(os=platform.system()):
    os = os.lower()
    if os == 'darwin':
        return 'Mac'
    if os == 'windows':
        return 'Windows'
    else:
        return 'Linux'


platform = get_platform()


# TODO: Adjust the sorting of these at some point.

SHOW_DEFAULT_CURRENCY = True

rounded_differently = {"BTC": 8,
                       "LTC": 8,
                       "BCH": 8,
                       "ADA": 6,
                       "DOGE": 8,
                       "DTO": 8,  # 10, but rounded to fit well
                       "ETH": 8,  # 18, but that does not fit on the window
                       "LINK": 8,  # 18, but that does not fit on the window
                       "UNI": 8  # 18, but that does not fit on the window
                       }


LATEST_XMR_AMOUNT = 1.01
LASTEST_USD_AMOUNT = monero_usd_price.calculate_usd_from_monero(monero_amount=LATEST_XMR_AMOUNT, print_price_to_console=False, monero_price=False)

CURRENT_PAYMENT_REQUEST = ''
SEND_TO_WALLET = '4Test5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4h4Test'
CURRENT_SEND_AMOUNT = ''
CURRENT_SEND_CURRENCY = ''
SELECTED_SUBSCRIPTION = ''

CURRENT_CREATE_PAYMENT_REQUEST_CURRENCY = ''

has_seen_welcome = False
