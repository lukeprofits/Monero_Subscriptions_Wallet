import requests
import json
import logging
from config import local_rpc_url, daemon_url
from src.logging import config as logging_config
from src.interfaces.observer import Observer
from src.interfaces.notifier import Notifier

class RPCClient(Notifier):
    _instance = None
    @classmethod
    def get(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._headers = None
        logging.config.dictConfig(logging_config)
        self.logger = logging.getLogger(self.__module__)
        self._observers = []
        self._balance = ''

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

    def current_block_height(self):
        result = self.daemon_post(self._current_block_height())
        return result['result']['height']

    def _current_block_height(self):
        return {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_info"
        }

    def get_version(self):
        result = self.post(self._get_version())
        return result.get("result", {}).get("version", False)

    def _get_version(self):
        return {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_version"
        }

    def local_healthcheck(self):
        try:
            return isinstance(self.get_version(), int)
        except requests.exceptions.ConnectionError as e:
            self.logger.debug(str(e))
            return False

    def refresh(self):
        try:
            return self.post(self._refresh())
        except requests.exceptions.ConnectionError as e:
            self.logger.debug(str(e))
            return False

    def _refresh(self):
        return {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "refresh"
        }

    def create_wallet(self):
        try:
            return self.post(self._create_wallet())
        except requests.exceptions.ConnectionError as e:
            self.logger.debug(str(e))
            return False

    def _create_wallet(self, filename='subscriptions_wallet'):
        return {
            "jsonrpc": "2.0",
            "id": "0",
            "method": 'create_wallet',
            "params": {
                "filename": filename,
                "language": "English"
            }
        }

    def open_wallet(self):
        try:
            return self.post(self._open_wallet())
        except requests.exceptions.ConnectionError as e:
            self.logger.debug(str(e))
            return False

    def _open_wallet(self, filename='subscriptions_wallet'):
        return {
            "jsonrpc": "2.0",
            "id": "0",
            "method": 'open_wallet',
            "params": {
                "filename": filename
            }
        }

    def get_address(self):
        try:
            return self.post(self._get_address())['result']['address']
        except requests.exceptions.ConnectionError as e:
            self.logger.debug(str(e))
            return False

    def _get_address(self):
        return {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_address",
        }

    def get_balance(self):
        try:
            self._balance = self.post(self._get_balance())['result']['balance']
            self.notify()
            return self._balance
        except requests.exceptions.ConnectionError as e:
            self.logger.debug(str(e))
            return False

    def _get_balance(self):
        return {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_balance"
        }

    def make_integrated_address(self, wallet, payment_id):
        try:
            return self.post(self._make_integrated_address(wallet, payment_id))['result']
        except requests.exceptions.ConnectionError as e:
            self.logger.debug(str(e))
            return False

    def _make_integrated_address(self, wallet, payment_id):
        return {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "make_integrated_address",
            "params": {
                "standard_address": wallet,
                "payment_id": payment_id
            }
        }

    def transfer(self, destination, amount):
        try:
            return self.post(self._transfer(destination, amount))['result']
        except requests.exceptions.ConnectionError as e:
            self.logger.debug(str(e))
            return False

    def _transfer(self, destination, amount):
        return {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "transfer",
            "params": {
                "destinations": {
                    'address': destination,
                    'amount': amount
                }
            }
        }

    @property
    def headers(self):
        if not self._headers:
            self._headers = {'Content-Type': 'application/json'}
        return self._headers

    def post(self, data):
        response = requests.post(local_rpc_url(), headers=self.headers, data=json.dumps(data))
        result = response.json()
        if 'error' in result:
            self.logger.error('Error: %s', result['error']['message'])
        return result

    def daemon_post(self, data):
        response = requests.post(daemon_url(), headers=self.headers, data=json.dumps(data))
        result = response.json()
        if 'error' in result:
            self.logger.error('Error: %s', result['error']['message'])
        return result
