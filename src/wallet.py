import os
import platform
import threading
import subprocess
import requests
import json
import monero_usd_price
import qrcode
import requests
from src.rpc_config import RPCConfig
from src.ui.common import CommonTheme
from src.rpc_client import RPCClient
from src.utils import valid_address

class Wallet():
    def __init__(self):
        self.name = "subscriptions_wallet"
        self.path = self._get_path()
        self._block_height = 0
        self._address = None
        self.config = RPCConfig()

    def _get_path(self):
        path = ''
        if not platform.system() == 'Windows':
            path = os.getcwd()
        return path

    def get_current_block_height(self):
        # Send the JSON-RPC request to the daemon
        return RPCClient().current_block_height()

    @property
    def block_height(self):
        if not self._block_height:
            if not self.exists():
                # If either file doesn't exist
                self.create()
            else:
                # If both files exist, do nothing
                print('Wallet exists already.')

            self._block_height = self.get_current_block_height()
        return self._block_height

    def exists(self):
        return os.path.isfile(f"{self.name}.keys") or os.path.isfile(self.name)

    def create(self):
        # Remove existing wallet if present
        try:
            os.remove(self.name)
        except:
            pass

        try:
            os.remove(f'{self.name}.keys')
        except:
            pass

        command = f"{self.config.cli_path} --generate-new-wallet {os.path.join(self.path, self.name)} --mnemonic-language English --command exit"
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Sending two newline characters, pressing 'Enter' twice
        process.stdin.write('\n')
        process.stdin.write('\n')
        process.stdin.flush()

        # Getting the output and error messages
        stdout, stderr = process.communicate()
        #print(stdout)
        #print(stderr)

        worked_check = process.returncode
        if worked_check == 0:
            output_text = stdout
            wallet_address = output_text.split('Generated new wallet: ')[1].split('View key: ')[0].strip()
            view_key = output_text.split('View key: ')[1].split('*********************')[0].strip()
            seed = output_text.split(' of your immediate control.')[1].split('********')[0].strip().replace('\n', '')
            print(f'wallet_address: {wallet_address}')
            print(f'view_key: {view_key}')
            print(f'seed: {seed}')

            with open(file=f'{self.name}_seed.txt', mode='a', encoding='utf-8') as f:
                f.write(f'Wallet Address:\n{wallet_address}\nView Key:\n{view_key}\nSeed:\n{seed}\n\nThe above wallet should not be your main source of funds. This is ONLY to be a side account for paying monthly subscriptions. If anyone gets access to this seed, they can steal all your funds. Please use responsibly.\n\n\n\n')

            return seed, wallet_address, view_key
        else:
            print(stderr)

    def address(self):
        if not self._address:
            result = RPCClient().fetch_address()
            if result is None:
                raise ValueError("Failed to get wallet address")

            self._address = result["address"]
            print(self._address)
        return self._address

    def balance(self):
        try:
            # get balance
            result = RPCClient().balance()

            if result is None:
                raise ValueError("Failed to get wallet balance")

            xmr_balance = monero_usd_price.calculate_monero_from_atomic_units(atomic_units=result["balance"])
            xmr_unlocked_balance = monero_usd_price.calculate_monero_from_atomic_units(atomic_units=result["unlocked_balance"])

            #print(xmr_unlocked_balance)

            try:
                usd_balance = format(monero_usd_price.calculate_usd_from_monero(float(xmr_balance)), ".2f")
            except:
                usd_balance = '---.--'

            #print(usd_balance)

            return xmr_balance, usd_balance, xmr_unlocked_balance

        except Exception as e:
            print(f'get_wallet_balance error: {e}')
            return '--.------------', '---.--'

    def send_subscription(self, subscription):
        self.send(address=subscription.sellers_wallet, amount=subscription.amount, payment_id=subscription.payment_id)

    def send(self, address, amount, payment_id=None):
        client = RPCClient()
        # this needs to measure in atomic units, not xmr, so this converts it.
        atomic_amount = monero_usd_price.calculate_atomic_units_from_monero(monero_amount=amount)

        if self.valid_format():
            print('Address is valid. Trying to send Monero')

            # Changes the wallet address to use an integrated wallet address ONLY if a payment id was specified.
            if payment_id:
                # generate the integrated address to pay (an address with the payment ID baked into it)
                address = client.create_integrated_address(sellers_wallet=address, payment_id=payment_id)

            result = client.send_payment(amount=atomic_amount, address=address)

            print('Sent Monero')

            if result is None:
                print('Failed to send Monero transaction')

        else:
            print('Wallet is not a valid monero wallet address.')

    def valid_format(self):
        return valid_address(self.address())

    def generate_qr(self):
        if self.valid_format():
            # Generate the QR code
            qr = qrcode.QRCode(version=1, box_size=3, border=4)
            qr.add_data("monero:" + self.address())
            qr.make(fit=True)
            theme = CommonTheme()
            qr_img = qr.make_image(fill_color=theme.monero_orange, back_color=theme.ui_overall_background)
            # Save the image to a file
            filename = "wallet_qr_code.png"
            with open(filename, "wb") as f:
                qr_img.save(f, format="PNG")
            return filename

        else:
            print('Monero Address is not valid')
            return None