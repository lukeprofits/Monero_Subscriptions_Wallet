import customtkinter as ctk
import styles
from src.interfaces.view import View
import config as cfg
from src.rpc_server import RPCServer
from lxml import html
import requests
import random
import json


def get_random_node():
    response = requests.get('https://monero.fail/')
    tree = html.fromstring(response.content)
    urls = tree.xpath('//span[@class="nodeURL"]/text()')
    random.shuffle(urls)  # mix them up so we get a random one instead of top to bottom.

    for url in urls:
        if '://' in url:
            url = url.split('://')[1]

        if ':' in url:  # make sure that it has the port
            print(url)
            if check_if_node_works(url):
                print(f'WORKS: {url}')
                return url


def check_if_node_works(node):
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


class NodeSelectionView(View):
    def build(self):
        self._app.geometry(styles.NODE_VIEW_GEOMETRY)

        # Back button and title
        styles.back_and_title(self, ctk, cfg, title=' Set Node:')

        self.node = ctk.StringVar(self._app, cfg.config_file.get('rpc', 'node_url'))
        self.node_selection = self.add(ctk.CTkEntry(self._app, textvariable=self.node, corner_radius=15, placeholder_text='xmr-node.cakewallet.com:18081'))
        self.node_selection.grid(row=1, column=0, columnspan=3, padx=70, pady=(25, 10), sticky="ew")

        # Frame to hold buttons
        center_frame = self.add(ctk.CTkFrame(self._app, ))
        center_frame.grid(row=2, column=0, columnspan=3, padx=0, pady=(10, 0), sticky="nsew")
        center_frame.columnconfigure([0, 1, 2, 3, 4, 5], weight=1)

        random_node = self.add(ctk.CTkButton(center_frame, text="Find Random Node", corner_radius=15, command=self.get_random_node_button_clicked))
        random_node.grid(row=0, column=2, padx=(10, 5), pady=0, sticky="ew")

        submit_button = self.add(ctk.CTkButton(center_frame, text="Save Settings", corner_radius=15, command=self.set_node))
        submit_button.grid(row=0, column=3, padx=(5, 10), pady=0, sticky="ew")

        info_text = "For best privacy, host your own node."
        info = self.add(ctk.CTkLabel(self._app, text=info_text))
        info.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def set_node(self):
        node = self.node_selection.get()
        rpc_server = RPCServer.get()
        config = cfg.config_file
        config.set(section='rpc', option='node_url', value=node)
        config.write()
        rpc_server.kill()
        rpc_server.start()
        rpc_server.failed_to_start = False
        rpc_server.check_readiness()
        self._app.switch_view('main')

    def get_random_node_button_clicked(self):
        # TODO: This feels messy. Consider refactoring.

        if self.node_selection:
            self.node_selection.destroy()

        please_wait_text = 'Please wait. Finding a random node...'
        self.node_selection = self.add(ctk.CTkEntry(self._app, corner_radius=15, placeholder_text=please_wait_text))
        self.node_selection.grid(row=1, column=0, columnspan=3, padx=70, pady=(25, 10), sticky="ew")

        self._app.update()  # refresh GUI

        if self.node_selection:
            self.node_selection.destroy()

        self.node_selection = self.add(ctk.CTkEntry(self._app, corner_radius=15, textvariable=ctk.StringVar(self._app, get_random_node())))
        self.node_selection.grid(row=1, column=0, columnspan=3, padx=70, pady=(25, 10), sticky="ew")
