from datetime import datetime

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

    def json_friendly(self):
        attributes = self.__dict__.copy()
        # attributes.pop('logger')
        # attributes.pop('rpc_client')
        # attributes.pop('wallet')
        attributes['start_date'] = attributes['start_date'].strftime(self.DATE_FORMAT)
        return attributes