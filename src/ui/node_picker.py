from kivy.uix.screenmanager import Screen
from src.ui.common import CommonTheme
from src.rpc_config import RPCConfig
from src.rpc_server import RPCServer
from src.wallet import Wallet
import random
import requests
import json
import threading
from lxml import html

class NodePicker(Screen):
    def __init__(self, **kwargs):
        super(NodePicker, self).__init__(**kwargs)
        wallet = Wallet()
        self.rpc_server = RPCServer(wallet)

    def add_node(self):
        node = self.ids.node.text
        if '://' in node:
            node = node.split('://')[1]

        if self._check_node(node):
            RPCConfig().set_node(self.ids.node.text)
            self.parent.current = 'loading'
        else:
            #Something to notify the user it didn't work
            self.ids.node.background_color = CommonTheme().monero_orange

    def add_random_node(self):
        node = self._get_random_node()
        RPCConfig().set_node(node)
        self.parent.current = 'loading'

    def _get_random_node(self):
        response = requests.get('https://monero.fail/')
        tree = html.fromstring(response.content)
        urls = tree.xpath('//span[@class="nodeURL"]/text()')
        random.shuffle(urls)  # mix them up so we get a random one instead of top to bottom.

        for url in urls:
            if '://' in url:
                url = url.split('://')[1]

            if ':' in url:  # make sure that it has the port
                print(url)
                if self._check_node(url):
                    print(f'WORKS: {url}')
                    return url


    def _check_node(self, node):
        url = f'http://{node}/json_rpc'
        headers = {'Content-Type': 'application/json'}
        payload = {
            'jsonrpc': '2.0',
            'id': '0',
            'method': 'get_info',
            'params': {}
        }

        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            result = response.json()

            if 'result' in result and 'status' in result['result'] and result['result']['status'] == 'OK':
                return True
            else:
                return False

        except requests.exceptions.RequestException as e:
            print(e)
            return False