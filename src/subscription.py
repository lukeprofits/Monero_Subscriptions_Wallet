"""
A class for each individual Subscription object
"""

import logging
import logging.config
from datetime import datetime, timedelta
import monerorequest
from sched import scheduler
from src.clients.rpc import RPCClient
from src.logging import config as logging_config
from config import send_payments
from src.exchange import Exchange

class Subscription:
    def __init__(self, custom_label, sellers_wallet, currency, amount,  payment_id, start_date, days_per_billing_cycle, number_of_payments, change_indicator_url=''):
        self.custom_label = custom_label if monerorequest.Check.name(custom_label) else ''
        self.sellers_wallet = sellers_wallet if monerorequest.Check.wallet(wallet_address=sellers_wallet, allow_standard=True, allow_integrated_address=False, allow_subaddress=False) else ''
        self.currency = currency if monerorequest.Check.currency(currency) else ''
        self.amount = amount if monerorequest.Check.amount(amount) else ''
        self.payment_id = payment_id if monerorequest.Check.payment_id(payment_id) else monerorequest.make_random_payment_id()
        if monerorequest.Check.start_date(start_date):
            start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            start_date = datetime.now()
        self.start_date = start_date
        self.days_per_billing_cycle = days_per_billing_cycle if monerorequest.Check.days_per_billing_cycle(days_per_billing_cycle) else 30
        self.number_of_payments = number_of_payments if monerorequest.Check.number_of_payments(number_of_payments) else 1
        self.change_indicator_url = change_indicator_url if monerorequest.Check.change_indicator_url(change_indicator_url) else ''
        logging.config.dictConfig(logging_config)
        self.logger = logging.getLogger(self.__module__)

    def json_friendly(self):
        json_data = {
            "custom_label": self.custom_label,
            "sellers_wallet": self.sellers_wallet,
            "currency": self.currency,
            "amount": self.amount,
            "payment_id": self.payment_id,
            "start_date":  monerorequest.convert_datetime_object_to_truncated_RFC3339_timestamp_format(self.start_date),
            "days_per_billing_cycle": self.days_per_billing_cycle,
            "number_of_payments": self.number_of_payments,
            "change_indicator_url": self.change_indicator_url
        }

        attributes = json_data

        return attributes

    def encode(self):
        monero_request = monerorequest.make_monero_payment_request(custom_label=self.custom_label,
                                sellers_wallet=self.sellers_wallet,
                                currency=self.currency,
                                amount=self.amount,
                                payment_id=self.payment_id,
                                start_date=monerorequest.convert_datetime_object_to_truncated_RFC3339_timestamp_format(self.start_date),
                                days_per_billing_cycle=self.days_per_billing_cycle,
                                number_of_payments=self.number_of_payments,
                                change_indicator_url=self.change_indicator_url)

        return monero_request

    def next_payment_time(self):
        next_time = self.start_date

        while next_time < datetime.now():
            next_time = next_time + timedelta(days=self.days_per_billing_cycle)
        return next_time

    @classmethod
    def decode(cls, code):
        subscription_data_as_json = monerorequest.Decode.monero_payment_request_from_code(monero_payment_request=code)

        return subscription_data_as_json

    def make_payment(self):
        if self.payable():
            if send_payments():
                client = RPCClient.get()
                integrated_address = client.make_integrated_address(self.sellers_wallet, self.payment_id)['integrated_address']
                transfer_result = client.transfer(integrated_address, self.amount)
                Exchange.refresh_prices()
                return transfer_result['amount'] == int(self.amount)
            else:
                self.logger.info('Sending Funds Disabled')
                return False
        else:
            self.logger.error('Insuffient Funds Balance: %s', Exchange.XMR_AMOUNT)
            return False

    def payable(self):
        Exchange.refresh_prices()
        xmr_to_send = Exchange.to_atomic_units(self.currency, float(self.amount))
        self.logger.info('Able to send funds %s XMR', xmr_to_send)
        return Exchange.to_atomic_units('XMR', Exchange.XMR_AMOUNT) > xmr_to_send

    def schedule(self):
        scheduler.enterabs(self.next_payment_time(), 1, self.make_payment)