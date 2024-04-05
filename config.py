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

NODE_URL = 'xmr-node.cakewallet.com:18081'

config_options = {
    'rpc': {
        'rpc_bind_port': 18088,
        'rpc_username': 'monero',
        'rpc_password': 'monero',
        'rpc': True,
        'local_rpc_url': 'http://127.0.0.1:18088/json_rpc',
        'node_url': NODE_URL,
        'cli_path': 'monero-wallet-cli',
        'daemon_url': f'{NODE_URL}/json_rpc',
        'wallet_dir': 'wallets'
    },
    'subscriptions': {
        'subs_file_path': 'Subscriptions.json'
    }
}

parser=argparse.ArgumentParser()
parser.add_argument('--subs-file-path')
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


'''
wallet_name = "subscriptions_wallet"
'''
# =====================
# Placeholders and Dynamic Values
# =====================
xmr_unlocked_balance = '--.------------'
wallet_balance_xmr = '--.------------'
wallet_balance_usd = '---.--'
current_monero_price = 150.00
wallet_address = ''
#'''

subscriptions = ''


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
# Longform Text
# =====================
welcome_popup_text = '''
           Welcome to the Monero Subscriptions Wallet!

We're thrilled that you've chosen to use our Free and Open Source Software (FOSS). Before you get started, there are a few important things you should know:

1. Monero Subscriptions Wallet is currently in alpha. Your feedback is valuable to us in making this software better. Please let us know if you encounter any issues or, if you are a developer, help resolve them! All the code is on GitHub.

2. Monero Subscriptions Wallet is intended to be a secondary wallet, rather than your primary one. As an internet-connected hot wallet, its security is only as robust as your computer's. We suggest using it as a side-wallet, maintaining just enough balance for your subscriptions.

3. Upon launching this software, you'll automatically have a $10/mo subscription that serves as a donation to the wallet developer. This helps us continue the development and maintenance of this FOSS project. If you do not want to donate to the developer, you are able to cancel this at any time by clicking on 'Cancel' next to the subscription, and the wallet will continue working as normal.

4. By using this software, you understand and agree that you're doing so at your own risk. The developers cannot be held responsible for any lost funds.

Enjoy using the Monero Subscriptions Wallet, thank you for your support, and if you are a Python developer, please consider helping us improve the project!

https://github.com/lukeprofits/Monero_Subscriptions_Wallet
'''

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
    SUBSCRIPTIONS_VIEW_GEOMETRY = '500x430'
    SUBSCRIPTIONS_VIEW_NO_SUBS_GEOMETRY = '500x195'
    RECEIVE_VIEW_GEOMETRY = '500x255'
    SET_CURRENCY_VIEW_GEOMETRY = '360x165'
    NODE_VIEW_GEOMETRY = '500x215'
    AMOUNT_VIEW_GEOMETRY = '500x195'

elif platform == 'Mac':
    BACK_BUTTON_EMOJI = '⬅'
    SETTINGS_BUTTON_EMOJI = '⚙'
    # Views
    MAIN_VIEW_GEOMETRY = '500x195'
    PAY_VIEW_GEOMETRY = '500x195'
    SETTINGS_VIEW_GEOMETRY = '500x205'
    SUBSCRIPTIONS_VIEW_GEOMETRY = '500x430'
    SUBSCRIPTIONS_VIEW_NO_SUBS_GEOMETRY = '500x195'
    RECEIVE_VIEW_GEOMETRY = '500x255'
    SET_CURRENCY_VIEW_GEOMETRY = '360x165'
    NODE_VIEW_GEOMETRY = '500x195'
    AMOUNT_VIEW_GEOMETRY = '500x195'

elif platform == 'Linux':
    BACK_BUTTON_EMOJI = '⬅'
    SETTINGS_BUTTON_EMOJI = '⚙'
    # Views
    MAIN_VIEW_GEOMETRY = '500x215'
    PAY_VIEW_GEOMETRY = '500x215'
    NODE_VIEW_GEOMETRY = '500x215'
    SETTINGS_VIEW_GEOMETRY = '500x215'
    SUBSCRIPTIONS_VIEW_GEOMETRY = '500x430'
    SUBSCRIPTIONS_VIEW_NO_SUBS_GEOMETRY = '500x195'
    RECEIVE_VIEW_GEOMETRY = '500x255'
    SET_CURRENCY_VIEW_GEOMETRY = '360x165'
    NODE_VIEW_GEOMETRY = '500x215'
    AMOUNT_VIEW_GEOMETRY = '500x195'

else:  # Right now this is unneeded because anything not mac/windows is assumed to be linux.
    BACK_BUTTON_EMOJI = '⬅'
    SETTINGS_BUTTON_EMOJI = '⚙'
    # Views
    MAIN_VIEW_GEOMETRY = '500x195'
    PAY_VIEW_GEOMETRY = '500x195'
    SETTINGS_VIEW_GEOMETRY = '500x205'
    SUBSCRIPTIONS_VIEW_GEOMETRY = '500x430'
    SUBSCRIPTIONS_VIEW_NO_SUBS_GEOMETRY = '500x195'
    RECEIVE_VIEW_GEOMETRY = '500x255'
    SET_CURRENCY_VIEW_GEOMETRY = '360x165'
    NODE_VIEW_GEOMETRY = '500x215'
    AMOUNT_VIEW_GEOMETRY = '500x195'

'''
# Set Monero Wallet CLI Path
if platform.system() == 'Windows':
    # Update path to the location of the monero-wallet-cli executable if your on WINDOWS
    monero_wallet_cli_path = "" + 'monero-wallet-cli.exe'
else:
    # Update path to the location of the monero-wallet-cli executable if your on other platforms
    monero_wallet_cli_path = os.getcwd() + '/' + 'monero-wallet-cli'

# Set Wallet Path
if platform.system() == 'Windows':
    wallet_file_path = ""
else:
    # Update this path to the location where you want to save the wallet file
    wallet_file_path = f'{os.getcwd()}/'
#'''

# TODO: Adjust the sorting of these at some point.
CURRENCY_OPTIONS = ["XMR", "BTC", "XGB", "XAU", "XAG", "USD", "EUR", "GBP", "CAD", "AUD", "CNY", "JPY", "KRW", "INR", "HKD", "BRL", "TWD", "CHF", "LTC", "BCH", "ADA", "DOGE", "DOT", "ETH", "LINK", "UNI"]

def add_fiat_currencies_to_currency_options():
    url = "https://raw.githubusercontent.com/datasets/currency-codes/master/data/codes-all.csv"
    column_name = "AlphabeticCode"
    response = requests.get(url)
    if response.status_code == 200:
        csv_data = StringIO(response.text)
        reader = csv.reader(csv_data)

        headers = next(reader)  # Get the header row
        if 'AlphabeticCode' in headers:
            code_index = headers.index(column_name)  # Find the index of the AlphabeticCode column

            for row in reader:
                if row:  # Make sure the row is not empty
                    currency_code = row[code_index]  # Use the index of AlphabeticCode
                    if currency_code not in CURRENCY_OPTIONS and currency_code != "":
                        CURRENCY_OPTIONS.append(currency_code)

add_fiat_currencies_to_currency_options()

SHOW_DEFAULT_CURRENCY = True
DEFAULT_CURRENCY = CURRENCY_OPTIONS[5]
SECONDARY_CURRENCY = CURRENCY_OPTIONS[0]


def currency_in_display_format(currency=DEFAULT_CURRENCY, amount=0):

    def check_for_symbol():
        if currency.upper() in symbols.keys():
            symbol = symbols[currency.upper()]
        else:
            symbol = ""
        return symbol

    has_ticker_after = ["XMR"]

    symbols = {"USD": "$",
               "BTC": "₿",
               "CYN": "¥",
               "EUR": "€",
               "JPY": "¥",
               "GBP": "£",
               "KRW": "₩",
               "INR": "₹",
               "CAD": "$",
               "HKD": "$",
               "AUD": "$"
               }

    # TODO: FORMAT AMOUNT TO THE PROPER NUMBER OF 0's

    return f"{check_for_symbol()}{amount} {currency.upper()}"


rounded_differently = {"BTC": 8,
                       "LTC": 8,
                       "BCH": 8,
                       "ADA": 6,
                       "DOGE": 8,
                       "DOT": 8,  # 10, but rounded to fit well
                       "ETH": 8,  # 18, but that does not fit on the window
                       "LINK": 8,  # 18, but that does not fit on the window
                       "UNI": 8  # 18, but that does not fit on the window
                       }


def get_value(currency_ticker, usd_value):
    def scrape_xe(currency_ticker):
        url = f"https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To={currency_ticker.upper()}"
        main_xpath = '//p[contains(text(), "1.00 US Dollar =")]/../p[2]'
        # Used to use: [contains(@class, "BigRate")] ...but that broke so switched to [2]

        response = requests.get(url)
        tree = html.fromstring(response.content)
        return tree.xpath(main_xpath)[0].text_content().strip().split(' ')[0].replace(',', '')

    def scrape_goldback_exchange_rate():
        url = 'https://www.goldback.com/exchange-rate'
        page_content = requests.get(url).text
        # Find the gb_average_exchange_rate constant's value
        usd_cost_for_one_goldback = re.search(r"gb_average_exchange_rate\s*=\s*'([\d.]+)';", page_content).group(1)
        dollar_value_in_goldbacks = Decimal(1) / Decimal(usd_cost_for_one_goldback)
        return dollar_value_in_goldbacks

    def round_to_two_decimal_places(value):
        final_decimal = Decimal(value)
        final_rounded = final_decimal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        formatted_value = format(final_rounded, ",.2f")
        return formatted_value

    # Skip conversion if the currency is XMR (no need)
    if currency_ticker.upper() == "XMR":
        return LATEST_XMR_AMOUNT

    # Skip conversion if the currency is USD (we already have it)
    elif currency_ticker.upper() == "USD":
        return usd_value

    # Goldbacks
    elif currency_ticker.upper() == "XGB":
        dollar_value_in_goldbacks = scrape_goldback_exchange_rate()
        final = Decimal(dollar_value_in_goldbacks) * Decimal(usd_value)
        return round_to_two_decimal_places(final)

    # Everything Else
    else:
        dollar_value_in_currency = scrape_xe(currency_ticker)
        final = Decimal(dollar_value_in_currency) * Decimal(usd_value)

        if currency_ticker not in rounded_differently.keys():
            final_rounded = round_to_two_decimal_places(final)
        else:
            rounding_spec = Decimal('1.' + ('0' * rounded_differently[currency_ticker]))
            final_rounded = final.quantize(rounding_spec, rounding=ROUND_HALF_UP)
            final_rounded = format(final_rounded, f",.{str(rounded_differently[currency_ticker])}f")

        # TODO: Consider chopping digits off the right if the length is longer than 12 so that it fits in the window.
        # Failed: PRB SLSH CKD NKR AFA -- check if we have these in the wallet or not.
        # Maybe get a list of all options from XE and then remove from the list if we don't have a conversion rate and not in the hard coded list?
        return str(final_rounded)


LATEST_XMR_AMOUNT = 1.01
LASTEST_USD_AMOUNT = monero_usd_price.calculate_usd_from_monero(monero_amount=LATEST_XMR_AMOUNT, print_price_to_console=False, monero_price=False)
WALLET_ADDRESS = '4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2S'
SEND_TO_WALLET = ''
monero_orange = '#ff6600'
ui_overall_background = '#1D1D1D'
HEADINGS_FONT_SIZE = (font, 20)
SUBHEADING_FONT_SIZE = (font, 16)
CURRENT_PAYMENT_REQUEST = ''


def back_and_title(self, ctk, cfg, title='Enter A Title'):
    # Title
    label = self.add(ctk.CTkLabel(self._app, text=title, font=cfg.HEADINGS_FONT_SIZE))
    label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

    # Back Button
    back_button = self.add(
        ctk.CTkButton(self._app, text=cfg.BACK_BUTTON_EMOJI, font=(cfg.font, 24), width=35, height=30,
                      command=self.open_main))
    back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")