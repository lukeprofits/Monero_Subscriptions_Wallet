"""
A class for each individual Subscription object
"""

from datetime import datetime
import monerorequest


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

    @classmethod
    def decode(cls, code):
        subscription_data_as_json = monerorequest.Decode.monero_payment_request_from_code(monero_payment_request=code)

        return subscription_data_as_json
