import requests
import json
import logging
from src.rpc_config import RPCConfig
from src.logging import config as logging_config

class RPCClient():
    def __init__(self):
        self.config = RPCConfig()
        self._headers = None
        logging.config.dictConfig(logging_config)
        self.logger = logging.getLogger(self.__module__)

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

    @property
    def headers(self):
        if not self._headers:
            self._headers = {'Content-Type': 'application/json'}
        return self._headers

    def post(self, data):
        response = requests.post(self.config.local_url, headers=self.headers, data=json.dumps(data))
        result = response.json()
        if 'error' in result:
            self.logger.error('Error:', result['error']['message'])
        return result

    def daemon_post(self, data):
        response = requests.post(self.config.daemon_url, headers=self.headers, data=json.dumps(data))
        result = response.json()
        if 'error' in result:
            self.logger.error('Error:', result['error']['message'])
        return result