import datetime
class RPCClientMock():
    def __init__(self):
        self._current_block_height = 0
        self._create_integrated_address = '888tNkZrPN6JsEgekjMnABU4TBzc2Dt29EPAvkRxbANsAnjyPbb3iQ1YBRk1UXcdRsiKc9dhwMVgN5S9cQUiyoogDavup3H'
        self._send_payment = True
        self._fetch_address = '888tNkZrPN6JsEgekjMnABU4TBzc2Dt29EPAvkRxbANsAnjyPbb3iQ1YBRk1UXcdRsiKc9dhwMVgN5S9cQUiyoogDavup3H'
        self._balance = {
            'balance': 2000000000000,
            'unlocked_balance': 2000000000000
        }
        self._transfers = [{
            'payment_id': '1a2b3c4d5e6f7a8b',
            'timestamp': datetime.datetime.timestamp(datetime.datetime.now())
        }]
        self._remote_info = {}
        self._get_version = 'v1.0'
        self._remote_healthcheck = True
        self._local_healthcheck = True

    def current_block_height(self, override = None):
        if override:
            self._current_block_height = override
        return self._current_block_height

    def create_integrated_address(self, sellers_wallet, payment_id, override = None):
        if override:
            self._create_integrated_address = override
        return self._create_integrated_address

    def send_payment(self, amount, address, override = None):
        if override:
            self._send_payment = override
        return self._send_payment

    def fetch_address(self, override = None):
        if override:
            self._fetch_address = override
        return self._fetch_address

    def balance(self, override = None):
        if override:
            self._balance = override
        return self._balance

    def transfers(self, override = None):
        if override:
            self._transfers = override
        return self._transfers

    def remote_info(self, override = None):
        if override:
            self._remote_info = override
        return self._remote_info

    def get_version(self, override = None):
        if override:
            self._get_version = override
        return self._get_version

    def remote_healthcheck(self, override):
        if override:
            self._remote_healthcheck = override
        return self._remote_healthcheck

    def local_healthcheck(self, override):
        if override:
            self._local_healthcheck = override
        return self._local_healthcheck