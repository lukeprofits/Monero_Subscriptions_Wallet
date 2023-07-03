import datetime
class RPCClientMock():
    def current_block_height(self):
        return 0

    def create_integrated_address(self):
        return '888tNkZrPN6JsEgekjMnABU4TBzc2Dt29EPAvkRxbANsAnjyPbb3iQ1YBRk1UXcdRsiKc9dhwMVgN5S9cQUiyoogDavup3H'

    def send_payment(self):
        return True

    def fetch_address(self):
        return '888tNkZrPN6JsEgekjMnABU4TBzc2Dt29EPAvkRxbANsAnjyPbb3iQ1YBRk1UXcdRsiKc9dhwMVgN5S9cQUiyoogDavup3H'

    def balance(self):
        return 0.0

    def transfers(self):
        return [{
            'payment_id': '1a2b3c4e5d6f7a8b',
            'destinations': [
                {
                    'address': '888tNkZrPN6JsEgekjMnABU4TBzc2Dt29EPAvkRxbANsAnjyPbb3iQ1YBRk1UXcdRsiKc9dhwMVgN5S9cQUiyoogDavup3H'
                }
            ],
            'timestamp': datetime.datetime.timestamp(datetime.datetime.now())
        }]

    def remote_info(self):
        return {}

    def get_version(self):
        return 'v1.0'

    def remote_healthcheck(self):
        return True

    def local_healthcheck(self):
        return True