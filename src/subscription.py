import json
from datetime import datetime
import gzip
import base64
import logging
from src.rpc_client import RPCClient
from src.utils import valid_address

class Subscription():
    DATE_FORMAT = "%Y-%m-%d"
    def __init__(self, custom_label, amount, billing_cycle_days, start_date, sellers_wallet, currency, payment_id=''):
        self.custom_label = custom_label
        self.amount = None
        if amount:
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
        self.logger = logging.getLogger(self.__module__)

    def determine_if_a_payment_is_due(self):
        # if today's date is before the subscription start date
        if datetime.now() <= self.start_date:
            return False, self.start_date

        for payment_id, dest_address, transaction_date in self.loop_transactions():
            if payment_id == self.payment_id and dest_address == self.make_integrated_address():
                # Check the date. See if it happened this billing cycle.
                days_left = self.check_date_for_how_many_days_until_payment_needed(transaction_date)
                if days_left > 0:  # renew when subscription expires
                    self.logger.info(f'Found a payment on {transaction_date}. No payment is due.')
                    return False, transaction_date  # It was this billing cycle. Payment is NOT due.

        # If we made it here without finding a payment this month, a payment is due.
        self.logger.info('Did not find a payment. A payment is due.')
        return True, ''

    def loop_transactions(self):
        try:  # Get all outgoing transfers from the wallet
            transfers = RPCClient().transfers()

        except Exception as e:
            self.logger.error(f"Error querying Monero RPC: {e}")
            return False, ''

        for t in transfers:
            if 'destinations' in t and 'payment_id' in t and 'timestamp' in t:  # if it has all the fields we are checking
                payment_id = t['payment_id']
                dest_address = t['destinations'][0]['address']  # DO NOT convert to integrated
                transaction_date = t['timestamp']
                transaction_date = datetime.fromtimestamp(transaction_date)
                yield(payment_id, dest_address, transaction_date)

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

        return days_left

    def renewal_date(self):
        for payment_id, dest_address, transaction_date in self.loop_transactions():
            days_left = self.check_date_for_how_many_days_until_payment_needed(transaction_date)
            return datetime.now() + days_left.days()
        return datetime.now().strftime(self.DATE_FORMAT)

    def currency_valid(self):
        # add more in the future as needed
        if self.currency == 'USD' or self.currency == 'XMR':
            return True
        else:
            return False

    def amount_valid(self):
        if type(self.amount) == int:
            return True

        elif type(self.amount) == float:
            if round(self.amount, 12) == self.amount:
                return True
            else:
                return False

        else:
            return False

    def payment_id_valid(self):
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

    def start_date_valid(self):
        return type(self.start_date) == datetime

    def billing_cycle_days_valid(self):
        return type(self.billing_cycle_days) == int

    def sellers_wallet_valid(self):
        return valid_address(self.sellers_wallet)

    def custom_label_valid(self):
        return True

    def valid_check(self):
        return self.payment_id_valid() and self.amount_valid() and self.currency_valid() and \
               self.sellers_wallet_valid() and self.billing_cycle_days_valid() and self.start_date_valid()

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

    @classmethod
    def decode(cls, code):
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