from src.ui.common import CommonTheme
from os import path
import PySimpleGUI as sg

class NodePicker(CommonTheme):
    NODE_FILENAME = 'node_to_use.txt'
    def node_picked(cls):
        return path.exists(cls.NODE_FILENAME)

    def picked_node(cls):
        with open(cls.NODE_FILENAME, 'r') as f:
            node = f.readline().strip()  # read first line into 'node'
        return node

    def pick_node(self):
        self._welcome_popup()
        self._main_window()
        self._picker_loop()

    def close_window(self):
        self._main_window.close()

    def _welcome_popup(self):
        sg.popup(self.WELCOME_POPUP_TEXT, icon=self.icon, no_titlebar=True, background_color=self.ui_overall_background, grab_anywhere=True)

    @property
    def _layout(self):
        if not self._layout:
            self._layout = [[sg.Column([
                [sg.Text("Add A Monero Node:", font=(self.font, 24), text_color=monero_orange, background_color=ui_overall_background)],
                [sg.Text("     For maximum privacy: Add your own node, or one run by someone you trust     \n", font=(self.font, 16), text_color=self.ui_sub_font, background_color=self.ui_overall_background)],
                [sg.Input(default_text='node.sethforprivacy.com:18089', key='custom_node', justification='center', size=(30, 2), font=(self.font, 18)), sg.Button('Add Node', key='add_node', font=(self.font, 12), size=(12, 1), button_color=(self.ui_button_b_font, self.ui_button_b))],
                [sg.Text('', font=(self.font, 4))],
                [sg.Text("...or if you have a typical threat model and face minimal risks, you can add a random node\n", font=(self.font, 12), text_color=self.ui_sub_font, background_color=self.ui_overall_background)],
                [sg.Button('          Add A Random Node          ', key='add_random_node', font=(self.font, 12), button_color=(self.ui_button_a_font, self.ui_button_a))],
                [sg.Text('')],
                [sg.Text("Random nodes pulled from: https://Monero.fail\n", font=(self.font, 10), text_color=self.monero_orange, background_color=self.ui_overall_background)],
                ], element_justification='c', justification='center')
            ]]
        return self._layout

    @property
    def _main_window(self):
        if not self._main_window:
            self._main_window = sg.Window('Node Input', self._layout, keep_on_top=False, no_titlebar=True, grab_anywhere=True)
        return self._main_window

    def _picker_loop(self):
        while True:
            event, values = self._main_window.read()
            if event == 'add_node':
                self._add_node(node)
                break

            elif event == 'add_random_node':
                self._add_random_node()
                break

            if event == sg.WIN_CLOSED:
                break

    def _add_node(self, values):
        node = values['custom_node']
        if '://' in node:
            node = node.split('://')[1]

        print(node)

        if self._check_if_node_works(node):
            self._main_window['custom_node'].update(value="Success!")

            # Save the node to the file
            with open(NODE_FILENAME, 'w') as f:
                f.write(node + '\n')

        else:
            self._main_window['custom_node'].update(value="Node did not respond. Try Another.")

    def _add_random_node(self):
        print('Adding a random node. Please wait. \nThe software will seem to be frozen until a node is found.')
        node = self._get_random_monero_node()
        # Save the node to the file
        with open(node_filename, 'w') as f:
            f.write(node + '\n')

    def _get_random_monero_node():
        response = requests.get('https://monero.fail/')
        tree = html.fromstring(response.content)
        urls = tree.xpath('//span[@class="nodeURL"]/text()')
        random.shuffle(urls)  # mix them up so we get a random one instead of top to bottom.

        for url in urls:
            if '://' in url:
                url = url.split('://')[1]

            if ':' in url:  # make sure that it has the port
                print(url)
                if self._check_if_node_works(url):
                    print(f'WORKS: {url}')
                    return url

    def _check_if_node_works(self, node):
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

    WELCOME_TEXT = '''
        Welcome to the Monero Subscriptions Wallet!

        We're thrilled that you've chosen to use our Free and Open Source Software (FOSS). Before you get started, there are a few important things you should know:

        1. Monero Subscriptions Wallet is currently in alpha. Your feedback is valuable to us in making this software better. Please let us know if you encounter any issues or, if you are a developer, help resolve them! All the code is on GitHub.

        2. Monero Subscriptions Wallet is intended to be a secondary wallet, rather than your primary one. As an internet-connected hot wallet, its security is only as robust as your computer's. We suggest using it as a side-wallet, maintaining just enough balance for your subscriptions.

        3. Upon launching this software, you'll automatically have a $10/mo subscription that serves as a donation to the wallet developer. This helps us continue the development and maintenance of this FOSS project. If you do not want to donate to the developer, you are able to cancel this at any time by clicking on 'Cancel' next to the subscription, and the wallet will continue working as normal.

        4. By using this software, you understand and agree that you're doing so at your own risk. The developers cannot be held responsible for any lost funds.

        Enjoy using the Monero Subscriptions Wallet, thank you for your support, and if you are a Python developer, please consider helping us improve the project!

        https://github.com/lukeprofits/Monero_Subscriptions_Wallet
    '''