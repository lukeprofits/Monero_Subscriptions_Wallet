import requests
import json
from src.rpc_config import RPCConfig

class RPCClient():
    def __init__(self):
        self.config = RPCConfig()
        self._headers = None

    def current_block_height(self):
        result = self.daemon_post(self._get_info())
        return result['result']['height']

    def create_integrated_address(self, sellers_wallet, payment_id):
        result = self.post(self._integrated_address_request(sellers_wallet, payment_id))
        return result['result']['integrated_address']

    def send_payment(self, address, amount):
        result = self.post(self._payment(address=address, amount=amount))
        return result.get("result")

    def fetch_address(self):
        result = self.post(self._address())
        return result.get("result")

    def balance(self):
        result = self.post(self._balance())
        return result.get("result")

    def transfers(self):
        result = self.post(self._transfers())
        return result.get("result", {}).get("out", {})

    def remote_info(self):
        result = self.daemon_post(self._get_info())
        return result.get("result", {})

    def get_version(self):
        result = self.post(self._get_version())
        return result.get("result", {}).get("version", False)

    def remote_healthcheck(self):
        try:
            info_hash = self.remote_info()
            return info_hash.get('synchronized', False)
        except requests.exceptions.ConnectionError:
            return False

    def local_healthcheck(self):
        try:
            return type(self.get_version()) == int
        except requests.exceptions.ConnectionError as e:
            print(str(e))
            return False

    def _get_version(self):
        return {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_version"
        }

    def _transfers(self):
        return {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_transfers",
            "params": {"out": True}
        }

    def _get_info(self):
        return {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_info"
        }

    def _balance(self):
        return {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_balance"
        }

    def _address(self):
        return {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_address"
        }

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

    def daemon_post(self, data):
        response = requests.post(self.config.daemon_url, headers=self.headers, data=json.dumps(data))
        result = response.json()
        if 'error' in result:
            print('Error:', result['error']['message'])
        return result
