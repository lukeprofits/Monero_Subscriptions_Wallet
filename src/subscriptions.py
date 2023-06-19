from os import path
import json
import requests
import monero_usd_price
from datetime import datetime
import time
from src.rpc_config import RPCConfig
from src.wallet import Wallet
from src.thread_manager import ThreadManager
import gzip
import base64
from src.rpc_client import RPCClient
from src.utils import valid_address

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

                time.sleep(60 * 1)  # run check every 1 min

            except Exception as e:
                print(f'Error in send_recurring_payments: {e}')

    def monero_from_usd(self, usd_amount, print_price_to_console=False):
        monero_price = monero_usd_price.median_price_not_threaded(print_price_to_console=print_price_to_console)
        monero_amount = round(usd_amount / monero_price, 12)
        if print_price_to_console:
            print(monero_amount)
        return monero_amount

class Subscription():
    DATE_FORMAT = "%Y-%m-%d"
    def __init__(self, custom_label, amount, billing_cycle_days, start_date, sellers_wallet, currency, payment_id=''):
        self.custom_label = custom_label
        self.amount = float(amount)
        if billing_cycle_days:
            self.billing_cycle_days = int(billing_cycle_days)
        else:
            self.billing_cycle_days = None
        self.payment_id = payment_id
        if start_date:
            self.start_date = datetime.strptime(start_date, self.DATE_FORMAT)
        else:
            self.start_date = datetime.now()
        self.currency = currency
        self.sellers_wallet = sellers_wallet

    def determine_if_a_payment_is_due(self):
        try:  # Get all outgoing transfers from the wallet
            transfers = RPCClient().transfers()

        except Exception as e:
            print(f"Error querying Monero RPC: {e}")
            return False, ''

        #print(f"Transfers: {transfers}")

        # Check each of them
        for t in transfers:
            if 'destinations' in t and 'payment_id' in t and 'timestamp' in t:  # if it has all the fields we are checking
                payment_id = t['payment_id']
                dest_address = t['destinations'][0]['address']  # we are reading the addresses. DO NOT convert to integrated
                transaction_date = t['timestamp']
                transaction_date = datetime.fromtimestamp(transaction_date)
                #print(f'\nFOUND: {payment_id}, {dest_address}, {transaction_date}\n')
                if payment_id == self.payment_id and dest_address == self.make_integrated_address():
                    # Check the date. See if it happened this billing cycle.
                    days_left = self.check_date_for_how_many_days_until_payment_needed(transaction_date)
                    if days_left > 0:  # renew when subscription expires
                        print(f'Found a payment on {transaction_date}. No payment is due.')
                        return False, transaction_date  # It was this billing cycle. Payment is NOT due.

        # if today's date is before the subscription start date
        if datetime.now() <= self.start_date:
            return False, self.start_date

        # If we made it here without finding a payment this month, a payment is due.
        print('Did not find a payment. A payment is due.')
        return True, ''

    def make_integrated_address(self):
        RPCClient().create_integrated_address(self.sellers_wallet, self.payment_id)

    def check_date_for_how_many_days_until_payment_needed(self, date):
        # Returns the number of days left.
        number_of_days = self.billing_cycle_days

        # if subscription start date is in the future
        if datetime.now() <= date:
            number_of_days = 0

        # Calculate the time difference in hours
        hours_difference = (datetime.now() - date).total_seconds() / (60 * 60)

        # Calculate the hours left
        hours_left = (number_of_days * 24) - hours_difference

        # Calculate the days left
        days_left = hours_left / 24

        # print(f'Days Left: {days_left}')
        # print(f'Hours Left: {hours_left}')

        return days_left

    def supported_currency(self):
        # add more in the future as needed
        if self.currency == 'USD' or self.currency == 'XMR':
            return True
        else:
            return False

    def amount_format(self):
        if type(self.amount) == int:
            return True

        elif type(self.amount) == float:
            if round(self.amount, 12) == self.amount:
                return True
            else:
                return False

        else:
            return False

    def valid_payment_id(self):
        if self.payment_id:
            if len(self.payment_id) != 16:
                return False

            valid_chars = set('0123456789abcdef')
            for char in self.payment_id:
                if char not in valid_chars:
                    return False

            # If it passed all these checks
            return True
        return True

    def valid_billing_cycle_days(self):
        return type(self.billing_cycle_days) == int

    def valid_wallet_format(self):
        return valid_address(self.sellers_wallet)

    def valid_check(self):
        return self.valid_payment_id() and self.amount_format() and self.supported_currency() and \
               self.valid_wallet_format() and self.valid_billing_cycle_days()

    def encode(self):
        # Convert the JSON data to a string
        json_str = self.to_json()

        # Compress the string using gzip compression
        compressed_data = gzip.compress(json_str.encode('utf-8'))

        # Encode the compressed data into a Base64-encoded string
        encoded_str = base64.b64encode(compressed_data).decode('ascii')

        # Add the Monero Subscription identifier
        monero_subscription = 'monero-subscription:' + encoded_str

        return monero_subscription

    def decode(self, code):
        # Catches user error. Code can start with "monero_subscription:", or ""
        code_parts = code.split('-subscription:')

        if len(code_parts) == 2:
            monero_subscription_data = code_parts[1]
        else:
            monero_subscription_data = code_parts[0]

        # Extract the Base64-encoded string from the second part of the code
        encoded_str = monero_subscription_data

        # Decode the Base64-encoded string into bytes
        compressed_data = base64.b64decode(encoded_str.encode('ascii'))

        # Decompress the bytes using gzip decompression
        json_bytes = gzip.decompress(compressed_data)

        # Convert the decompressed bytes into a JSON string
        json_str = json_bytes.decode('utf-8')

        # Parse the JSON string into a Python object
        subscription_data_as_json = json.loads(json_str)

        return subscription_data_as_json

    def to_json(self):
        return json.dumps(self.json_friendly())

    def json_friendly(self):
        attributes = self.__dict__.copy()
        attributes['start_date'] = attributes['start_date'].strftime(self.DATE_FORMAT)
        return attributes