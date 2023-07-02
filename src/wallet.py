import os
import platform
import subprocess
import monero_usd_price
import qrcode
import logging
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
        self.median_usd_price = None
        self.logger = logging.getLogger(self.__module__)

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
                self.logger.info('Wallet exists already.')

            self._block_height = self.get_current_block_height()
        return self._block_height

    def exists(self):
        return os.path.isfile(self.name) and os.path.isfile(f'{self.name}.keys')

    def create(self):
        # Remove existing wallet if present
        try:
            os.remove(self.name)
        except os.IOError:
            pass

        try:
            os.remove(f'{self.name}.keys')
        except os.IOError:
            pass

        command = f"{self.config.cli_path} --generate-new-wallet {os.path.join(self.path, self.name)}"
        command += " --mnemonic-language English --command exit"
        process = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Sending two newline characters, pressing 'Enter' twice
        process.stdin.write('\n')
        process.stdin.write('\n')
        process.stdin.flush()

        # Getting the output and error messages
        stdout, stderr = process.communicate()

        self.logger.info(stdout)
        self.logger.error(stderr)

        worked_check = process.returncode
        if worked_check == 0:
            output_text = stdout
            wallet_address = output_text.split('Generated new wallet: ')[1].split('View key: ')[0].strip()
            view_key = output_text.split('View key: ')[1].split('*********************')[0].strip()
            seed = output_text.split(' of your immediate control.')[1].split('********')[0].strip().replace('\n', '')
            self.logger.info(f'wallet_address: {wallet_address}')
            self.logger.info(f'view_key: {view_key}')
            self.logger.info(f'seed: {seed}')

            with open(file=f'{self.name}_seed.txt', mode='a', encoding='utf-8') as f:
                message = f'Wallet Address:\n{wallet_address}\nView Key:\n{view_key}\nSeed:\n{seed}\n\n'
                message += 'The above wallet should not be your main source of funds. '
                message += 'This is ONLY to be a side account for paying monthly subscriptions. '
                message += 'If anyone gets access to this seed, they can steal all your funds. Please use responsibly.'
                f.write(message)

            return seed, wallet_address, view_key
        else:
            self.logger.error(stderr)

    def address(self):
        if not self._address:
            result = RPCClient().fetch_address()
            if result is None:
                raise ValueError("Failed to get wallet address")

            self._address = result["address"]
            self.logger.info(self._address)
        return self._address

    def balance(self):
        try:
            # get balance
            result = RPCClient().balance()

            if result is None:
                raise ValueError("Failed to get wallet balance")

            xmr_balance = monero_usd_price.calculate_monero_from_atomic_units(atomic_units=result["balance"])
            self.logger.info(f'XMR Balance: {xmr_balance}')
            xmr_unlocked_balance = \
                monero_usd_price.calculate_monero_from_atomic_units(atomic_units=result["unlocked_balance"])
            try:
                usd_balance = format(self.calculate_usd_exchange(float(xmr_balance)), ".2f")
            except ValueError:
                usd_balance = 0

            return xmr_balance, usd_balance, xmr_unlocked_balance

        except Exception as e:
            self.logger.error(f'get_wallet_balance error: {e}')
            return 0, 0, 0

    def calculate_usd_exchange(self, amount):
        self.logger.info(f'Median USD Price: {self.median_usd_price}')
        if not self.median_usd_price:
            self.median_usd_price = monero_usd_price.median_price()
            self.logger.info(f'Median USD Price After: {self.median_usd_price}')

        usd_amount = round(amount * self.median_usd_price, 2)

        return usd_amount

    def amount_available(self, amount, currency):
        balance = self.balance()
        if currency == 'USD':
            available_balance = balance[1]
        elif currency == 'XMR':
            available_balance = balance[2]
        if amount > float(available_balance):
            return False

        return True

    def send_subscription(self, subscription):
        self.send(address=subscription.sellers_wallet, amount=subscription.amount, payment_id=subscription.payment_id)

    def send(self, address, amount, payment_id=None):
        client = RPCClient()
        # this needs to measure in atomic units, not xmr, so this converts it.
        atomic_amount = monero_usd_price.calculate_atomic_units_from_monero(monero_amount=amount)

        if valid_address(address):
            self.logger.info('Address is valid. Trying to send Monero')

            # Changes the wallet address to use an integrated wallet address ONLY if a payment id was specified.
            if payment_id:
                # generate the integrated address to pay (an address with the payment ID baked into it)
                address = client.create_integrated_address(sellers_wallet=address, payment_id=payment_id)

            result = client.send_payment(amount=atomic_amount, address=address)

            self.logger.info('Sent Monero')

            if result is None:
                self.logger.error('Failed to send Monero transaction')
                return False

            return True
        else:
            self.logger.info('Wallet is not a valid monero wallet address.')
            return False

    def valid_format(self):
        return valid_address(self.address())

    def generate_qr(self):
        if self.valid_format():
            # Generate the QR code
            qr = qrcode.QRCode(version=1, box_size=3, border=4)
            qr.add_data("monero:" + self.address())
            qr.make(fit=True)
            theme = CommonTheme()
            qr_img = qr.make_image(fill_color=theme.monero_orange_hex, back_color=theme.ui_overall_background_hex)
            # Save the image to a file
            filename = "wallet_qr_code.png"
            with open(filename, "wb") as f:
                qr_img.save(f, format="PNG")
            return filename

        else:
            self.logger.info('Monero Address is not valid')
            return None