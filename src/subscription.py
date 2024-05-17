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

class Subscription:
    def __init__(self, custom_label, sellers_wallet, currency, amount,  payment_id, start_date, days_per_billing_cycle, number_of_payments, change_indicator_url=''):
        self.custom_label = custom_label if monerorequest.Check.name(custom_label) else ''
        self.sellers_wallet = sellers_wallet if monerorequest.Check.wallet(wallet_address=sellers_wallet, allow_standard=True, allow_integrated_address=False, allow_subaddress=False) else ''
        self.currency = currency if monerorequest.Check.currency(currency) else ''
        self.amount = amount if monerorequest.Check.amount(amount) else ''
        self.payment_id = payment_id if monerorequest.Check.payment_id(payment_id) else monerorequest.make_random_payment_id()
        self.start_date = start_date if monerorequest.Check.start_date(start_date) else monerorequest.convert_datetime_object_to_truncated_RFC3339_timestamp_format(datetime.now())
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
            "start_date": self.start_date,
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
                                start_date=self.start_date,
                                days_per_billing_cycle=self.days_per_billing_cycle,
                                number_of_payments=self.number_of_payments,
                                change_indicator_url=self.change_indicator_url)

        return monero_request

    def next_payment_time(self):
        next_time = datetime.strptime(self.start_date, '%Y-%m-%dT%H:%M:%S.%fZ')

        while next_time < datetime.now():
            next_time = next_time + timedelta(days=self.days_per_billing_cycle)
        return next_time

    @classmethod
    def decode(cls, code):
        subscription_data_as_json = monerorequest.Decode.monero_payment_request_from_code(monero_payment_request=code)

        return subscription_data_as_json

    def make_payment(self):
        xmr_to_send = Exchange.to_atomic_units(self.currency, self.amount)
        if Exchange.XMR_AMOUNT > xmr_to_send:
            logger.info('Sending Funds %s XMR', xmr_to_send)
            if send_payments():
                client = RPCClient()
                integrated_address = client.make_integrated_address(self.sellers_wallet, self.payment_id)['integrated_address']
                client.transfer(integrated_address, self.amount)
            else:
                logger.info('Sending Funds Disabled')
        else:
            logger.error('Insuffient Funds Attempted to Send: %s Balance: %s', xmr_to_send, Exchange.XMR_AMOUNT)
        #Last step
        Exchange.refresh_prices()

    def schedule(self):
        scheduler.enterabs(self.next_payment_time(), 1, self.make_payment)