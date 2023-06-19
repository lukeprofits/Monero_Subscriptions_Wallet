import requests
import json
from src.rpc_config import RPCConfig

class RPCClient():
    def __init__(self):
        self.config = RPCConfig()
        self._headers = None

    def create_integrated_address(self, sellers_wallet, payment_id):
        result = self.post(self._integrated_address_request(sellers_wallet, payment_id))
        return result['result']['integrated_address']

    def send_payment(self, address, amount):
        result = self.post(self._payment(address=address, amount=amount))
        return result.get("result")

    def _payment(self, address, amount):
        return {
                "jsonrpc": "2.0",
                "id": "0",
                "method": "transfer",
                "params": {
                    "destinations": [{"amount": amount, "address": address}],
                    "priority": 1,
                    #"ring_size": 11,
                    "get_tx_key": True
                }
            }

    def _integrated_address_request(self, sellers_wallet, payment_id):
        return {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "make_integrated_address",
            "params": {
                "standard_address": sellers_wallet,
                "payment_id": payment_id
            }
        }

    @property
    def headers(self):
        if not self._headers:
            self._headers = {'Content-Type': 'application/json'}
        return self._headers

    def post(self, data):
        response = requests.post(self.config.local_url, headers=self.headers, data=json.dumps(data))
        result = response.json()
        if 'error' in result:
            print('Error:', result['error']['message'])
        return result