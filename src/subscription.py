from datetime import datetime
import base64
import gzip
import json


class Subscription:
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

    def __init__(self, custom_label, amount, days_per_billing_cycle, start_date, sellers_wallet, currency, number_of_payments, payment_id='', change_indicator_url=''):
        self.custom_label = custom_label
        self.amount = float(amount)
        if days_per_billing_cycle:
            self.days_per_billing_cycle = int(days_per_billing_cycle)
        else:
            self.days_per_billing_cycle = None
        self.payment_id = payment_id
        if start_date:
            self.start_date = datetime.fromisoformat(start_date)
        else:
            self.start_date = datetime.now()
        self.currency = currency
        self.sellers_wallet = sellers_wallet
        self.number_of_payments = number_of_payments
        self.change_indicator_url = change_indicator_url

    def json_friendly(self):
        attributes = self.__dict__.copy()
        # attributes.pop('logger')
        # attributes.pop('rpc_client')
        # attributes.pop('wallet')
        attributes['start_date'] = attributes['start_date'].strftime(self.DATE_FORMAT)
        return attributes

    def encode(self):
        # Convert the JSON data to a string
        json_str = self.to_json()

        # Compress the string using gzip compression
        compressed_data = gzip.compress(json_str.encode('utf-8'))

        # Encode the compressed data into a Base64-encoded string
        encoded_str = base64.b64encode(compressed_data).decode('ascii')

        # Add the Monero Subscription identifier
        monero_subscription = 'monero-request:' + encoded_str

        return monero_subscription

    @classmethod
    def decode(cls, code):
        # Catches user error. Code can start with "monero_subscription:", or ""
        code_parts = code.split('-request:1:')

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
