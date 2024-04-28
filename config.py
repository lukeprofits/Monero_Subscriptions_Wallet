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

NODE_URL = 'xmr-node.cakewallet.com:18081'

config_options = {
    'rpc': {
        'rpc_bind_port': 18088,
        'rpc_username': 'monero',
        'rpc_password': 'monero',
        'rpc': False,
        'local_rpc_url': 'http://127.0.0.1:18088/json_rpc',
        'node_url': NODE_URL,
        'daemon_url': f'{NODE_URL}/json_rpc',
        'wallet_dir': 'wallets'
    },
    'subscriptions': {
        'subscriptions': [],
        'default_currency': 'USD',
        'secondary_currency': 'XMR'
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
#'''


'''
window = ''
start_block_height = None
supported_currencies = ["USD", "XMR"]
withdraw_to_wallet = ''

# =====================
# Flags and Booleans
# =====================
rpc_is_ready = False
stop_flag = threading.Event()  # Define a flag to indicate if the threads should stop

# =====================
# Theme Variables
# =====================
# Hex Colors
ui_title_bar = '#222222'
ui_button_a = '#F96800'
ui_button_a_font = '#F0FFFF'
ui_button_b = '#716F74'
ui_button_b_font = '#FFF9FB'
ui_main_font = '#F4F6EE'
ui_sub_font = '#A7B2C7'
ui_lines = '#696563'
ui_outline = '#2E2E2E'
ui_barely_visible = '#373737'
ui_regular = '#FCFCFC'
monero_grey = '#4c4c4c'
monero_white = '#FFFFFF'
monero_grayscale_top = '#7D7D7D'
monero_grayscale_bottom = '#505050'
main_text = ui_main_font  # this lets separators be orange but text stay white
subscription_text_color = ui_sub_font
subscription_background_color = ui_overall_background  # cfg.ui_title_bar

# Set Theme
icon = 'icon.ico'
'''

font = 'Nunito Sans'

'''
title_bar_text = 'Monero Subscriptions Wallet'
icon_png_path = "./icon.png"

#'''

# =====================
# Platform-Dependent Configurations
# =====================


def get_platform(os=platform.system()):
    os = os.lower()
    if os == 'darwin':
        return 'Mac'
    if os == 'windows':
        return 'Windows'
    else:
        return 'Linux'


platform = get_platform()


if platform == 'Windows':
    BACK_BUTTON_EMOJI = '⏴'
    SETTINGS_BUTTON_EMOJI = '☰'
    # Views
    MAIN_VIEW_GEOMETRY = '500x215'
    PAY_VIEW_GEOMETRY = '500x215'
    SETTINGS_VIEW_GEOMETRY = '500x215'
    SUBSCRIPTIONS_VIEW_GEOMETRY = '500x325'
    SUBSCRIPTIONS_VIEW_NO_SUBS_GEOMETRY = '500x195'
    RECEIVE_VIEW_GEOMETRY = '500x325'
    SET_CURRENCY_VIEW_GEOMETRY = '360x165'
    NODE_VIEW_GEOMETRY = '500x215'
    AMOUNT_VIEW_GEOMETRY = '500x195'
    REVIEW_REQUEST_VIEW_GEOMETRY = '500x215'
    WELCOME_VIEW_GEOMETRY = '500x480'

elif platform == 'Mac':
    BACK_BUTTON_EMOJI = '⬅'
    SETTINGS_BUTTON_EMOJI = '⚙'
    # Views
    MAIN_VIEW_GEOMETRY = '500x200'
    PAY_VIEW_GEOMETRY = '500x200'
    SETTINGS_VIEW_GEOMETRY = '500x205'
    SUBSCRIPTIONS_VIEW_GEOMETRY = '500x325'
    SUBSCRIPTIONS_VIEW_NO_SUBS_GEOMETRY = '500x200'
    RECEIVE_VIEW_GEOMETRY = '500x325'
    SET_CURRENCY_VIEW_GEOMETRY = '360x165'
    NODE_VIEW_GEOMETRY = '500x200'
    AMOUNT_VIEW_GEOMETRY = '500x200'
    REVIEW_REQUEST_VIEW_GEOMETRY = '500x215'
    WELCOME_VIEW_GEOMETRY = '500x480'

elif platform == 'Linux':
    BACK_BUTTON_EMOJI = '⬅'
    SETTINGS_BUTTON_EMOJI = '⚙'
    # Views
    MAIN_VIEW_GEOMETRY = '500x200'
    PAY_VIEW_GEOMETRY = '500x200'
    SETTINGS_VIEW_GEOMETRY = '500x210'
    SUBSCRIPTIONS_VIEW_GEOMETRY = '500x325'
    SUBSCRIPTIONS_VIEW_NO_SUBS_GEOMETRY = '500x195'
    RECEIVE_VIEW_GEOMETRY = '500x325'
    SET_CURRENCY_VIEW_GEOMETRY = '360x165'
    NODE_VIEW_GEOMETRY = '500x215'
    AMOUNT_VIEW_GEOMETRY = '500x195'
    REVIEW_REQUEST_VIEW_GEOMETRY = '500x215'
    WELCOME_VIEW_GEOMETRY = '500x480'

else:  # Right now this is unneeded because anything not mac/windows is assumed to be linux.
    BACK_BUTTON_EMOJI = '⬅'
    SETTINGS_BUTTON_EMOJI = '⚙'
    # Views
    MAIN_VIEW_GEOMETRY = '500x195'
    PAY_VIEW_GEOMETRY = '500x195'
    SETTINGS_VIEW_GEOMETRY = '500x205'
    SUBSCRIPTIONS_VIEW_GEOMETRY = '500x325'
    SUBSCRIPTIONS_VIEW_NO_SUBS_GEOMETRY = '500x195'
    RECEIVE_VIEW_GEOMETRY = '500x325'
    SET_CURRENCY_VIEW_GEOMETRY = '360x165'
    NODE_VIEW_GEOMETRY = '500x215'
    AMOUNT_VIEW_GEOMETRY = '500x195'
    REVIEW_REQUEST_VIEW_GEOMETRY = '500x215'
    WELCOME_VIEW_GEOMETRY = '500x480'


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
monero_orange = '#ff6600'
ui_overall_background = '#1D1D1D'

HEADINGS_FONT_SIZE = (font, 26)
BIGGER_SUBHEADING_FONT_SIZE = (font, 20)
SUBHEADING_FONT_SIZE = (font, 16)
BODY_FONT_SIZE = (font, 14)
CURRENT_PAYMENT_REQUEST = ''
SEND_TO_WALLET = ''
CURRENT_SEND_AMOUNT = ''
CURRENT_SEND_CURRENCY = ''
SELECTED_SUBSCRIPTION = ''

has_seen_welcome = False


def back_and_title(self, ctk, cfg, title='Enter A Title', pad_bottom=0):
    # Title
    label = self.add(ctk.CTkLabel(self._app, text=title, font=HEADINGS_FONT_SIZE))
    label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, pad_bottom), sticky="ew")

    # Back Button
    back_button = self.add(ctk.CTkButton(self._app, text=BACK_BUTTON_EMOJI, font=(cfg.font, 24), width=35, height=30, command=self.open_main))
    back_button.grid(row=0, column=0, padx=10, pady=(10, pad_bottom), sticky="w")
