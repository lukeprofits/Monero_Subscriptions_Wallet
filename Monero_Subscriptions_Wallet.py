import os
import time
import json
import gzip
import psutil
import base64
import qrcode
import random
import requests
import threading
import pyperclip
import subprocess
from lxml import html
import monero_usd_price
import PySimpleGUI as sg
from datetime import datetime
import platform


# OVERALL FUNCTIONS ####################################################################################################
def kill_everything():
    global stop_flag

    print('\n\n Please close this terminal window and relaunch the Monero Subscriptions Wallet')

    stop_flag.set()  # Stop threads gracefully

    # Kill the program
    current_process = psutil.Process(os.getpid())  # Get the current process ID
    current_process.terminate()  # Terminate the current process and its subprocesses


def find_matching_subscription_index(subscriptions, custom_label, amount, billing_cycle_days):
    for index, subscription in enumerate(subscriptions):
        if (subscription['custom_label'] == custom_label and
            subscription['amount'] == amount and
            subscription['billing_cycle_days'] == billing_cycle_days):
            return index
    return None


def send_recurring_payments():
    while not stop_flag.is_set():
        try:
            subscriptions = read_subscriptions()

            print('Checking if subscriptions need to be paid.')

            for sub in subscriptions:
                payment_is_due, payment_date = determine_if_a_payment_is_due(sub)

                if payment_is_due:
                    sellers_wallet = sub["sellers_wallet"]
                    currency = sub["currency"]
                    amount = sub["amount"]
                    payment_id = sub["payment_id"]

                    if currency == 'USD':
                        print('SENDING USD')
                        xmr_amount = monero_usd_price.calculate_monero_from_usd(usd_amount=amount)
                        print(f'Sending {xmr_amount} XMR to {sellers_wallet} with payment ID {payment_id}')
                        send_monero(destination_address=sellers_wallet, amount=xmr_amount, payment_id=payment_id)

                    elif currency == 'XMR':
                        print('SENDING XMR')
                        print(f'Sending {amount} XMR to {sellers_wallet} with payment ID {payment_id}')
                        send_monero(destination_address=sellers_wallet, amount=amount, payment_id=payment_id)

            print('Checking subscriptions again in 1 min')

            time.sleep(60 * 1)  # run check every 1 min

        except Exception as e:
            print(f'Error in send_recurring_payments: {e}')


# MAKE FUNCTIONS #######################################################################################################
def make_payment_id():
    payment_id = ''.join([random.choice('0123456789abcdef') for _ in range(16)])
    return payment_id


def make_integrated_address(payment_id, merchant_public_wallet_address):
    global local_rpc_url

    headers = {'Content-Type': 'application/json'}
    data = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": "make_integrated_address",
        "params": {
            "standard_address": merchant_public_wallet_address,
            "payment_id": payment_id
        }
    }

    response = requests.post(f"{local_rpc_url}", headers=headers, data=json.dumps(data))
    result = response.json()

    if 'error' in result:
        print('Error:', result['error']['message'])

    else:
        integrated_address = result['result']['integrated_address']
        return integrated_address


def make_subscription_code(json_data):
    # Convert the JSON data to a string
    json_str = json.dumps(json_data)

    # Compress the string using gzip compression
    compressed_data = gzip.compress(json_str.encode('utf-8'))

    # Encode the compressed data into a Base64-encoded string
    encoded_str = base64.b64encode(compressed_data).decode('ascii')

    # Add the Monero Subscription identifier
    monero_subscription = 'monero-subscription:' + encoded_str

    return monero_subscription


def create_subscription(custom_label='Subscription', payment_id='', sellers_wallet='', currency='', amount=0.00, billing_cycle_days=None, start_date=None):
    if check_if_payment_id_is_valid(payment_id):
        if check_if_monero_wallet_address_is_valid_format(sellers_wallet):
            if check_if_currency_is_supported(currency):
                if check_if_amount_is_proper_format(amount):
                    if type(billing_cycle_days) == int:
                        if not start_date:
                            subscription = {
                                "custom_label": custom_label,
                                "sellers_wallet": sellers_wallet,
                                "currency": currency,
                                "amount": amount,
                                "payment_id": payment_id,
                                "start_date": datetime.now().strftime("%Y-%m-%d"),
                                "billing_cycle_days": billing_cycle_days
                                }
                            return subscription

                        else:  # if we added a start date
                            subscription = {
                                "custom_label": custom_label,
                                "sellers_wallet": sellers_wallet,
                                "currency": currency,
                                "amount": amount,
                                "payment_id": payment_id,
                                "start_date": start_date,
                                "billing_cycle_days": billing_cycle_days
                            }
                            return subscription

                    else:
                        print(f'Not a valid number of days: {billing_cycle_days}')
                else:
                    print(f'Not a valid amount: {amount}')
            else:
                print(f'Not a supported currency: {currency}')
        else:
            print(f'Not a valid seller_wallet: {sellers_wallet}')
    else:
        print(f'Not a valid payment ID: {payment_id}')


def create_wallet(wallet_name):  # Using CLI Wallet
    global monero_wallet_cli_path, wallet_file_path

    # Remove existing wallet if present
    try:
        os.remove(wallet_name)
    except:
        pass

    try:
        os.remove(f'{wallet_name}.keys')
    except:
        pass

    command = f"{monero_wallet_cli_path} --generate-new-wallet {os.path.join(wallet_file_path, wallet_name)} --mnemonic-language English --command exit"
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

        with open(file=f'{wallet_name}_seed.txt', mode='a', encoding='utf-8') as f:
            f.write(f'Wallet Address:\n{wallet_address}\nView Key:\n{view_key}\nSeed:\n{seed}\n\nThe above wallet should not be your main source of funds. This is ONLY to be a side account for paying monthly subscriptions. If anyone gets access to this seed, they can steal all your funds. Please use responsibly.\n\n\n\n')

        return seed, wallet_address, view_key
    else:
        print(stderr)


def generate_monero_qr(wallet_address):
    if check_if_monero_wallet_address_is_valid_format(wallet_address):
        # Generate the QR code
        qr = qrcode.QRCode(version=1, box_size=3, border=4)
        qr.add_data("monero:" + wallet_address)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color=monero_orange, back_color=ui_overall_background)
        # Save the image to a file
        filename = "wallet_qr_code.png"
        with open(filename, "wb") as f:
            qr_img.save(f, format="PNG")
        return filename

    else:
        print('Monero Address is not valid')
        return None


# CHECK FUNCTIONS ######################################################################################################
def check_if_wallet_exists():
    global wallet_name

    if not os.path.isfile(f"{wallet_name}.keys") or not os.path.isfile(wallet_name):
        # If either file doesn't exist
        start_block_height = get_current_block_height()
        create_wallet(wallet_name=wallet_name)
        return start_block_height

    else:
        # If both files exist, do nothing
        print('Wallet exists already.')
        return None


def check_date_for_how_many_days_until_payment_needed(date, number_of_days):
    # Returns the number of days left.

    # if subscription start date is in the future
    if datetime.now() <= date:
        number_of_days = 0

    # Calculate the time difference in hours
    hours_difference = (datetime.now() - date).total_seconds() / (60 * 60)

    # Calculate the hours left
    hours_left = (number_of_days * 24) - hours_difference

    # Calculate the days left
    days_left = hours_left / 24

    # print(f'Days Left: {days_left}')
    # print(f'Hours Left: {hours_left}')

    return days_left


def check_if_currency_is_supported(currency):
    # add more in the future as needed
    if currency == 'USD' or currency == 'XMR':
        return True
    else:
        return False


def check_if_amount_is_proper_format(amount):
    if type(amount) == int:
        return True

    elif type(amount) == float:
        if round(amount, 12) == amount:
            return True
        else:
            return False

    else:
        return False


def check_if_monero_wallet_address_is_valid_format(wallet_address):
    # Check if the wallet address starts with the number 4
    if wallet_address[0] != "4":
        return False

    # Check if the wallet address is exactly 95 or 106 characters long
    if len(wallet_address) not in [95, 106]:
        return False

    # Check if the wallet address contains only valid characters
    valid_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    for char in wallet_address:
        if char not in valid_chars:
            return False

    # If it passed all these checks
    return True


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


def check_if_payment_id_is_valid(payment_id):
    if len(payment_id) != 16:
        return False

    valid_chars = set('0123456789abcdef')
    for char in payment_id:
        if char not in valid_chars:
            return False

    # If it passed all these checks
    return True


def determine_if_a_payment_is_due(subscription):
    global local_rpc_url

    try:  # Get all outgoing transfers from the wallet
        headers = {"Content-Type": "application/json"}
        data = {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_transfers",
            "params": {"out": True},
        }

        # Get outgoing payments
        response = requests.post(local_rpc_url, headers=headers, data=json.dumps(data))
        transfers = response.json()["result"]["out"]

    except Exception as e:
        print(f"Error querying Monero RPC: {e}")
        return False, ''

    #print(f"Transfers: {transfers}")

    # Check each of them
    for t in transfers:
        if 'destinations' in t and 'payment_id' in t and 'timestamp' in t:  # if it has all the fields we are checking
            payment_id = t['payment_id']
            dest_address = t['destinations'][0]['address']  # we are reading the addresses. DO NOT convert to integrated
            transaction_date = t['timestamp']
            transaction_date = datetime.fromtimestamp(transaction_date)
            #print(f'\nFOUND: {payment_id}, {dest_address}, {transaction_date}\n')
            if payment_id == subscription["payment_id"] and dest_address == make_integrated_address(payment_id=payment_id, merchant_public_wallet_address=subscription["sellers_wallet"]):
                # Check the date. See if it happened this billing cycle.
                days_left = check_date_for_how_many_days_until_payment_needed(transaction_date, subscription["billing_cycle_days"])
                if days_left > 0:  # renew when subscription expires
                    print(f'Found a payment on {transaction_date}. No payment is due.')
                    return False, transaction_date  # It was this billing cycle. Payment is NOT due.

    # if today's date is before the subscription start date
    subscription_start_date = datetime.strptime(subscription["start_date"], "%Y-%m-%d")
    if datetime.now() <= subscription_start_date:
        return False, subscription_start_date

    # If we made it here without finding a payment this month, a payment is due.
    print('Did not find a payment. A payment is due.')
    return True, ''


# CONVERSION FUNCTIONS #################################################################################################
def decode_monero_subscription_code(monero_subscription_code):
    # Catches user error. Code can start with "monero_subscription:", or ""
    code_parts = monero_subscription_code.split('-subscription:')

    if len(code_parts) == 2:
        monero_subscription_data = code_parts[1]
    else:
        monero_subscription_data = code_parts[0]

    # Extract the Base64-encoded string from the second part of the code
    encoded_str = monero_subscription_data

    # Decode the Base64-encoded string into bytes
    compressed_data = base64.b64decode(encoded_str.encode('ascii'))

    # Decompress the bytes using gzip decompression
    json_bytes = gzip.decompress(compressed_data)

    # Convert the decompressed bytes into a JSON string
    json_str = json_bytes.decode('utf-8')

    # Parse the JSON string into a Python object
    subscription_data_as_json = json.loads(json_str)

    return subscription_data_as_json


# RPC FUNCTIONS ########################################################################################################
def kill_monero_wallet_rpc():
    
    global rpc_is_ready
    
    if platform.system() == 'Windows':
        process = subprocess.Popen("tasklist", stdout=subprocess.PIPE)
        rpc_path = 'monero-wallet-rpc.exe'
    else:
        process = subprocess.Popen("ps", stdout=subprocess.PIPE)
        rpc_path = 'monero-wallet-r'
    out, err = process.communicate()

    for line in out.splitlines():
        if rpc_path.encode() in line:
            if platform.system() == 'Windows':
                pid = int(line.split()[1].decode("utf-8"))
            else:
                pid = int(line.split()[0].decode("utf-8"))
            os.kill(pid, 9)
            print(f"Successfully killed monero-wallet-rpc with PID {pid}")
            rpc_is_ready = False
            break

        else:
            print("monero-wallet-rpc process not found")


def start_local_rpc_server_thread():
    global wallet_name, host, port, rpc_is_ready, start_block_height, rpc_bind_port
    
    cmd = f'{os.getcwd()}/monero-wallet-rpc --wallet-file {wallet_name} --password "" --rpc-bind-port {rpc_bind_port} --disable-rpc-login --confirm-external-bind --daemon-host {host} --daemon-port {port}'
    
    if start_block_height:
        command = f'{monero_wallet_cli_path} --wallet-file {os.path.join(wallet_file_path, wallet_name)} --password "" --restore-height {start_block_height} --command exit'
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        blocks_synced = False

        while not blocks_synced:
            output = proc.stdout.readline().decode("utf-8").strip()

            print(f'SYNCING BLOCKS:{output}')

            if "Opened wallet:" in output:
                blocks_synced = True
                break

            if proc.poll() is not None:
                break

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        output = process.stdout.readline().decode("utf-8").strip()
        print(f'RPC STARTING:{output}')

        if "Starting wallet RPC server" in output:
            rpc_is_ready = True
            break

        if process.poll() is not None:
            break


def start_local_rpc_server():
    kill_monero_wallet_rpc()
    rpc_server_thread = threading.Thread(target=start_local_rpc_server_thread)
    rpc_server_thread.start()


def get_current_block_height():
    global daemon_rpc_url

    # Set up the JSON-RPC request
    headers = {'content-type': 'application/json'}
    data = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": "get_info"
    }

    # Send the JSON-RPC request to the daemon
    response = requests.post(daemon_rpc_url, data=json.dumps(data), headers=headers)

    # Parse the response to get the block height
    if response.status_code == 200:
        response_data = response.json()
        block_height = response_data["result"]["height"]
        print(f'Block Height: {block_height}')
        return block_height

    else:
        return None


def get_wallet_balance():
    global local_rpc_url, rpc_username, rpc_password

    headers = {"content-type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": "get_balance"
    }

    try:
        # get balance
        response = requests.post(local_rpc_url, headers=headers, data=json.dumps(payload), auth=(rpc_username, rpc_password))
        response.raise_for_status()
        result = response.json().get("result")

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

        return xmr_balance, usd_balance

    except Exception as e:
        print(f'get_wallet_balance error: {e}')
        return '--.------------', '---.--'


def get_wallet_address():
    global local_rpc_url, rpc_username, rpc_password

    headers = {"content-type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": "get_address"
    }

    response = requests.post(local_rpc_url, headers=headers, data=json.dumps(payload), auth=(rpc_username, rpc_password))
    response.raise_for_status()
    result = response.json().get("result")

    if result is None:
        raise ValueError("Failed to get wallet address")

    address = result["address"]
    print(address)
    return address


def send_monero(destination_address, amount, payment_id=None):
    global local_rpc_url, rpc_username, rpc_password

    # this needs to measure in atomic units, not xmr, so this converts it.
    amount = monero_usd_price.calculate_atomic_units_from_monero(monero_amount=amount)

    if check_if_monero_wallet_address_is_valid_format(wallet_address=destination_address):
        print('Address is valid. Trying to send Monero')

        # Changes the wallet address to use an integrated wallet address ONLY if a payment id was specified.
        if payment_id:
            # generate the integrated address to pay (an address with the payment ID baked into it)
            destination_address = make_integrated_address(payment_id=payment_id, merchant_public_wallet_address=destination_address)

        headers = {"content-type": "application/json"}
        payload = {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "transfer",
            "params": {
                "destinations": [{"amount": amount, "address": destination_address}],
                "priority": 1,
                #"ring_size": 11,
                "get_tx_key": True
            }
        }

        response = requests.post(local_rpc_url, headers=headers, data=json.dumps(payload), auth=(rpc_username, rpc_password))
        response.raise_for_status()
        result = response.json().get("result")

        print('Sent Monero')

        if result is None:
            print('Failed to send Monero transaction')

    else:
        print('Wallet is not a valid monero wallet address.')


# GUI FUNCTIONS ########################################################################################################
def subscription_added_popup():
    sg.popup("Subscription Added:\n\nWallet will now exit. Please relaunch.\n", no_titlebar=True, font=(font, 10), background_color=ui_overall_background)


def subscription_removed_popup():
    sg.popup("Subscription Canceled:\n\nWallet will now exit. Please relaunch.\n", no_titlebar=True, font=(font, 10), background_color=ui_overall_background)


def create_subscription_rows(subscriptions):
    result = []

    for i, sub in enumerate(subscriptions):
        amount = sub["amount"]
        custom_label = sub['custom_label']
        renews_in = sub["billing_cycle_days"]
        currency = sub["currency"]

        payment_is_due, payment_date = determine_if_a_payment_is_due(sub)  # hopefully this does not make booting slow

        if not payment_is_due and payment_date:
            days = check_date_for_how_many_days_until_payment_needed(date=payment_date, number_of_days=renews_in)
            renews_in = round(days)

        if currency == 'USD':
            currency_indicator_left = '$'
            currency_indicator_right = ' USD'

        elif currency == 'XMR':
            currency_indicator_left = ''
            currency_indicator_right = ' XMR'

        else:
            currency_indicator_left = ''
            currency_indicator_right = currency

        row = [
            sg.Text(f'    {currency_indicator_left}{amount}{currency_indicator_right}', justification='left', size=(12, 1), text_color=subscription_text_color, background_color=subscription_background_color),
            sg.Column([[sg.Text((custom_label + ''), justification='center', size=(None, 1), text_color=subscription_text_color, background_color=subscription_background_color)]], expand_x=True),
            sg.Text(f'Renews in {renews_in} day(s)', justification='right', size=(16, 1), text_color=subscription_text_color, background_color=subscription_background_color),
            sg.Button("Cancel", size=(7, 1), key=f'cancel_subscription_{i}', button_color=(ui_regular, ui_barely_visible)),
        ]
        result.append(row)

    return result


def create_subscription_layout(subscriptions):
    subscription_rows = create_subscription_rows(subscriptions)
    return [*subscription_rows, [sg.Column([[sg.Button("Add New Subscription", size=(40, 1), key='add_subscription', pad=(10, 10))]], expand_x=True, element_justification='center')]]


def update_gui_balance():
    global wallet_balance_xmr, wallet_balance_usd, wallet_address

    while not stop_flag.is_set():
        try:
            # Get the wallet balance info
            wallet_balance_xmr, wallet_balance_usd = get_wallet_balance()

            # Update the GUI with the new balance info
            if not wallet_balance_usd == '---.--':
                window['wallet_balance_in_usd'].update(f'        Balance:  ${wallet_balance_usd} USD')

            window['wallet_balance_in_xmr'].update(f'        XMR: {wallet_balance_xmr}')

            # Wait before updating again
            time.sleep(5)

        except Exception as e:
            print(f'Exception in thread "update_gui_balance: {e}"')


def read_subscriptions():
    global subs_file_path

    if not os.path.exists(subs_file_path):
        return []

    with open(subs_file_path, "r") as file:
        subscriptions = json.load(file)

    # Sort subscriptions by billing_cycle_days
    subscriptions.sort(key=lambda x: x['billing_cycle_days'])

    return subscriptions


def add_subscription(subscription):
    global subs_file_path

    if subscription:
        subscriptions = read_subscriptions()
        subscriptions.append(subscription)

        with open(subs_file_path, "w") as file:
            json.dump(subscriptions, file, indent=2)


def remove_subscription(subscriptions_list):
    subscriptions = subscriptions_list

    with open(subs_file_path, "w") as file:
        json.dump(subscriptions, file, indent=2)


def make_transparent():
    # Make the main window transparent
    window.TKroot.attributes('-alpha', 0.00)


def make_visible():
    # Make the main window transparent
    window.TKroot.attributes('-alpha', 1.00)


def add_subscription_from_merchant():
    global subscriptions, subscription_rows

    dev_sub_code = 'monero-subscription:H4sIACsJZGQC/12OXU+DMBSG/wrh2pkCAzPvYICJRhO36eZuSFvOBrEfpC3T1vjfbXfpuTrnfZ/kOT8xnbWRvGOYAIvvo3iPGQMT1XABJidQUS0FNqMU8U0Ua/Cl0t3XFQr4sjTZIVeXdzvt5OnMZ3hZ6dWrUa7fQF7N0Cr9WR7H5K6SH2RwVkvn5HNbFW4vdk/9w7oov5uSNE1OXbvJBr89Es2XwxoO6TZI6awUCGqD7m1bhwhzOYvgT9At8veELQdhurEPEPo3188NVqbrsYFApCjNFihfJEXoyMjYKM4dtZSBZ6z2TIZ+/wAVPrHVHQEAAA=='

    layout = [
        [sg.Column([
            [sg.Text("Paste Subscription Code Below", font=(font, 18), text_color=ui_sub_font)],
        ], justification='center', background_color=ui_title_bar)],
        [sg.Column([
            [sg.Text("")],
            [sg.Multiline(size=(60, 8), key="subscription_info", do_not_clear=False, autoscroll=False, default_text=dev_sub_code)],
            [sg.Button("    Add Subscription    ", key="add_merchant_subscription"), sg.Button("    Cancel    ", key="cancel_merchant_subscription", button_color=(ui_regular, ui_barely_visible))]
        ], element_justification='c', justification='center')]
    ]

    window = sg.Window(title_bar_text, layout=layout, modal=True, margins=(20, 20), background_color=ui_title_bar, titlebar_icon='', no_titlebar=True, use_custom_titlebar=True, grab_anywhere=True, icon=icon)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "cancel_merchant_subscription":
            break

        elif event == "add_merchant_subscription":
            subscription_info = values["subscription_info"]
            subscription_info = subscription_info.strip()  # in case user added any spaces or new lines

            # Check if the user submitted a dictionary rather than a monero-subscription code
            if '{' in subscription_info[0] and '}' in subscription_info[len(subscription_info)-1]:
                try:
                    subscription_json = json.loads(subscription_info)
                    add_subscription(subscription_json)
                    subscription_added_popup()
                    kill_everything()

                except:
                    print('JSON for subscription is not valid. Not adding.')

            else:  # Assume that the user submitted a monero-subscription code
                try:
                    subscription_json = decode_monero_subscription_code(subscription_info)
                    add_subscription(subscription_json)
                    subscription_added_popup()
                    kill_everything()

                except:
                    print('Monero subscription code is not valid. Not adding.')

            break

    window.close()


def add_subscription_manually():
    today = datetime.today().strftime("%Y-%m-%d")
    layout = [
        [sg.Column([
            [sg.Text("Enter Subscription Details", font=(font, 18), text_color=ui_sub_font)],
        ], justification='center', background_color=ui_title_bar)],
        [sg.Column([
            [sg.Text("")],
            [sg.Text("Custom Name:", background_color=ui_overall_background), sg.Input(size=(35, 1), key="custom_label")],
            [sg.Text("Amount:", background_color=ui_overall_background), sg.Input(size=(15, 1), key="amount", default_text='0.00'), sg.Combo(["USD", "XMR"], default_value="USD", key="currency")],
            [sg.Text("Billing Every:", background_color=ui_overall_background), sg.Input(size=(3, 1), key="billing_cycle_days"), sg.Text("Day(s)", background_color=ui_overall_background)],
            [sg.Text("Start Date (YYYY-MM-DD):", background_color=ui_overall_background), sg.Input(default_text=today, size=(10, 1), key="start_date")],
            [sg.Text("Seller's Wallet:", background_color=ui_overall_background), sg.Input(size=(102, 1), key="sellers_wallet")],
            [sg.Text("Optional Payment ID From Seller:", background_color=ui_overall_background), sg.Input(size=(20, 1), key="payment_id")],
            [sg.Text("")],
            [sg.Column([
                [sg.Button("    Add Subscription    ", key="add_manual_subscription"), sg.Button("    Cancel    ", key="cancel_manual_subscription", button_color=(ui_regular, ui_barely_visible))]
                ], justification='center', element_justification='c')]
        ], element_justification='l')]
    ]

    window = sg.Window(title_bar_text, layout=layout, modal=True, margins=(20, 20), titlebar_icon='', no_titlebar=True, background_color=ui_title_bar, use_custom_titlebar=True, grab_anywhere=True, icon=icon)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == "cancel_manual_subscription":
            break

        elif event == "add_manual_subscription":
            custom_label = values["custom_label"]
            amount = float(values["amount"])
            currency = values["currency"]
            billing_cycle_days = int(values["billing_cycle_days"])
            start_date = values["start_date"]
            sellers_wallet = values["sellers_wallet"]

            try:
                payment_id = values["payment_id"]
            except:
                payment_id = None

            if not payment_id:
                # '0000000000000000' is the same as no payment_id, but you want to use one.
                # (Without one, you can't make multiple payments at the same time to the same wallet address.)
                payment_id = make_payment_id()  # generates a random payment ID.

            subscription_info = make_subscription_code(create_subscription(custom_label=custom_label, amount=amount, currency=currency, billing_cycle_days=billing_cycle_days, start_date=start_date, sellers_wallet=sellers_wallet, payment_id=payment_id))
            subscription_json = decode_monero_subscription_code(subscription_info)
            add_subscription(subscription_json)

            print(custom_label)
            print(amount)
            print(currency)
            print(billing_cycle_days)
            print(start_date)
            print(sellers_wallet)
            print(payment_id)
            print(subscription_info)

            subscription_added_popup()
            kill_everything()
            break

    window.close()


def get_random_monero_node():
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


# THEME VARIABLES ######################################################################################################

# Hex Colors
ui_title_bar = '#222222'
ui_overall_background = '#1D1D1D'
ui_button_a = '#F96800'
ui_button_a_font = '#F0FFFF'
ui_button_b = '#716F74'
ui_button_b_font = '#FFF9FB'
ui_main_font = '#F4F6EE'
ui_sub_font = '#A7B2C7'
ui_lines = '#696563'
ui_outline = '#2E2E2E'
ui_barely_visible = '#373737'
ui_regular = '#FCFCFC'
monero_grey = '#4c4c4c'
monero_orange = '#ff6600'
monero_white = '#FFFFFF'
monero_grayscale_top = '#7D7D7D'
monero_grayscale_bottom = '#505050'

# Set Theme
icon = 'icon.ico'
font = 'Nunito Sans'
title_bar_text = ''
sg.theme('DarkGrey2')
# Modify the colors you want to change
sg.theme_background_color(ui_overall_background)  # MAIN BACKGROUND COLOR
sg.theme_button_color((ui_button_a_font, ui_button_a))  # whiteish, blackish
sg.theme_text_color(monero_orange)  # HEADING TEXT AND DIVIDERS
main_text = ui_main_font  # this lets separators be orange but text stay white
subscription_text_color = ui_sub_font
subscription_background_color = ui_overall_background  # ui_title_bar
sg.theme_text_element_background_color(ui_title_bar)  # Text Heading Boxes
sg.theme_element_background_color(ui_title_bar)  # subscriptions & transactions box color
sg.theme_element_text_color(ui_sub_font)  # My Subscriptions Text Color
sg.theme_input_background_color(ui_title_bar)
sg.theme_input_text_color(monero_orange)
sg.theme_border_width(0)
sg.theme_slider_border_width(0)

# VARIABLES ############################################################################################################
if platform.system() == 'Windows':
    monero_wallet_cli_path = "" + 'monero-wallet-cli.exe'  # Update path to the location of the monero-wallet-cli executable if your on WINDOWS
else:
    monero_wallet_cli_path = os.getcwd() + '/' + 'monero-wallet-cli'  # Update path to the location of the monero-wallet-cli executable if your on LINUX
wallet_name = "subscriptions_wallet"
wallet_file_path = f'{os.getcwd()}/'  # Update this path to the location where you want to save the wallet file
subs_file_path = 'Subscriptions.json'
rpc_bind_port = '18082'
local_rpc_url = f"http://127.0.0.1:{rpc_bind_port}/json_rpc"
rpc_username = "monero"
rpc_password = "monero"

stop_flag = threading.Event()  # Define a flag to indicate if the threads should stop

# Get subscriptions list
subscriptions = read_subscriptions()

welcome_popup_text = '''
           Welcome to the Monero Subscriptions Wallet!

We're thrilled that you've chosen to use our Free and Open Source Software (FOSS). Before you get started, there are a few important things you should know:

1. Monero Subscriptions Wallet is currently in alpha. Your feedback is valuable to us in making this software better. Please let us know if you encounter any issues or, if you are a developer, help resolve them! All the code is on GitHub.

2. Monero Subscriptions Wallet is intended to be a secondary wallet, rather than your primary one. As an internet-connected hot wallet, its security is only as robust as your computer's. We suggest using it as a side-wallet, maintaining just enough balance for your subscriptions.

3. We're currently experiencing minor visual update issues when a subscription is added or canceled. As a temporary workaround, the wallet will close and need to be restarted after adding/canceling a subscription. We're working hard to resolve this!

4. Upon launching this software, you'll automatically have a $10/mo subscription that serves as a donation to the wallet developer. This helps us continue the development and maintenance of this FOSS project. If you do not want to donate to the developer, you are able to cancel this at any time by clicking on 'Cancel' next to the subscription, and the wallet will continue working as normal.

5. By using this software, you understand and agree that you're doing so at your own risk. The developers cannot be held responsible for any lost funds.

Enjoy using the Monero Subscriptions Wallet, thank you for your support, and if you are a Python developer, please consider helping us improve the project!

https://github.com/lukeprofits/Monero_Subscriptions_Wallet
'''

# ADD DAEMON/NODE ######################################################################################################
node_filename = "node_to_use.txt"

if os.path.exists(node_filename):
    with open(node_filename, 'r') as f:
        node = f.readline().strip()  # read first line into 'node'
else:
    # welcome popup
    sg.popup(welcome_popup_text, icon=icon, no_titlebar=True, background_color=ui_overall_background, grab_anywhere=True)

    # Define the window's layout
    layout = [[sg.Column([
        [sg.Text("Add A Monero Node:", font=(font, 24), text_color=monero_orange, background_color=ui_overall_background)],
        [sg.Text("     For maximum privacy: Add your own node, or one run by someone you trust     \n", font=(font, 16), text_color=ui_sub_font, background_color=ui_overall_background)],
        [sg.Input(default_text='node.sethforprivacy.com:18089', key='custom_node', justification='center', size=(30, 2), font=(font, 18)), sg.Button('Add Node', key='add_node', font=(font, 12), size=(12, 1), button_color=(ui_button_b_font, ui_button_b))],
        [sg.Text('', font=(font, 4))],
        [sg.Text("...or if you have a typical threat model and face minimal risks, you can add a random node\n", font=(font, 12), text_color=ui_sub_font, background_color=ui_overall_background)],
        [sg.Button('          Add A Random Node          ', key='add_random_node', font=(font, 12), button_color=(ui_button_a_font, ui_button_a))],
        [sg.Text('')],
        [sg.Text("Random nodes pulled from: https://Monero.fail\n", font=(font, 10), text_color=monero_orange, background_color=ui_overall_background)],
        ], element_justification='c', justification='center')
    ]]

    # Create the window
    window = sg.Window('Node Input', layout, keep_on_top=True, no_titlebar=True, grab_anywhere=True)

    # Event loop
    while True:
        event, values = window.read()
        if event == 'add_node':
            node = values['custom_node']

            if '://' in node:
                node = node.split('://')[1]

            print(node)

            if check_if_node_works(node):
                window['custom_node'].update(value="Success!")

                # Save the node to the file
                with open(node_filename, 'w') as f:
                    f.write(node + '\n')
                break

            else:
                window['custom_node'].update(value="Node did not respond. Try Another.")

        elif event == 'add_random_node':
            print('Adding a random node. Please wait. \nThe software will seem to be frozen until a node is found.')
            node = get_random_monero_node()
            # Save the node to the file
            with open(node_filename, 'w') as f:
                f.write(node + '\n')
            break

        if event == sg.WIN_CLOSED:
            break

    window.close()

host = node.split(':')[0]
port = node.split(':')[1]

daemon_rpc_url = f"http://{host}:{port}/json_rpc"

# START PREREQUISITES ##################################################################################################
start_block_height = check_if_wallet_exists()  # auto-create one if it doesn't exist

rpc_is_ready = False
start_local_rpc_server()

# Set up the PySimpleGUI "please wait" popup window
layout = [
    [sg.Text("Please Wait: Monero RPC Server Is Starting", key="wait_text", font=(font, 18), background_color=ui_overall_background)],
    [sg.Text("                                   This may take a few minutes on first launch.", key="wait_text2", font=(font, 10), background_color=ui_overall_background)]
          ]

window = sg.Window("Waiting", layout, finalize=True, keep_on_top=True, no_titlebar=True, grab_anywhere=True)

while not rpc_is_ready:
    # Check for window events
    event, values = window.read(timeout=100)  # Read with a timeout so the window is updated

print('\n\nRPC Server has started')

wallet_balance_xmr = '--.------------'
wallet_balance_usd = '---.--'
wallet_address = get_wallet_address()

try:
    wallet_balance_xmr, wallet_balance_usd = get_wallet_balance()
except:
    pass

# Start a thread to send the payments
threading.Thread(target=send_recurring_payments).start()

# GUI LAYOUT ###########################################################################################################
subscription_layout = create_subscription_layout(subscriptions)
subscriptions_column = sg.Column(subscription_layout, key='subscriptions_column', pad=(10, 10))
frame = sg.Frame('My Subscriptions', layout=[[subscriptions_column]], key='subscriptions_frame', element_justification='center', pad=(10, 10), background_color=subscription_background_color)

# Define the window layout
layout = [
    [sg.Text("Monero Subscriptions Wallet", font=(font, 24), expand_x=True, justification='center', relief=sg.RELIEF_RIDGE, size=(None, 1), pad=(0, 0), text_color=main_text, background_color=ui_overall_background)],
    [sg.Text("Subscriptions will be paid automatically if the wallet remains open", font=("Helvetica", 10), expand_x=True, justification='center', background_color=ui_overall_background, pad=(0, 0))],
    [sg.Text("", font=(font, 8))],
        [
            sg.Column(
                [
                    ########
                    [sg.Text(f'        Balance:  ${wallet_balance_usd} USD', size=(25, 1), font=(font, 18), key='wallet_balance_in_usd', text_color=ui_sub_font, background_color=ui_overall_background)],
                    [sg.Text(f'        XMR: {wallet_balance_xmr}', size=(25, 1), font=(font, 18), key='wallet_balance_in_xmr', background_color=ui_overall_background)],
                    ########

                    ########
                    [frame],
                    ########

                ], element_justification='center', expand_x=True, expand_y=True
            ),
            sg.VerticalSeparator(pad=(0, 10)),
            sg.Column(
                [

                    ########
                    [sg.Text('Deposit XMR:', size=(20, 1), font=(font, 18), justification='center', text_color=ui_sub_font, background_color=ui_overall_background)],
                    [sg.Column([
                        [sg.Image(generate_monero_qr(wallet_address), size=(147, 147), key='qr_code', pad=(10, 0))],  # Placeholder for the QR code image
                        [sg.Button("Copy Address", size=(16, 1), key='copy_address', pad=(10, 10))]],
                        element_justification='center', pad=(0, 0))],
                    ########

                ], expand_x=True, expand_y=True, element_justification='c'
            )
        ],
        [sg.Text("", font=(font, 8), expand_x=True, justification='center', size=(None, 1), pad=(0, 0), text_color=main_text, background_color=ui_overall_background)],

        ########
        [sg.Column([
            [sg.Text(f'      Send XMR:', size=(12, 1), font=(font, 14), pad=(10, 10), text_color=ui_sub_font, background_color=ui_overall_background),
            sg.InputText(default_text='[ Enter a wallet address ]', key='withdraw_to_wallet', pad=(10, 10), justification='center', size=(46, 1)),
            sg.InputText(default_text=' [ Enter an amount ]', key='withdraw_amount', pad=(10, 10), justification='center', size=(20, 1)),
            sg.Button("Send", size=(8, 1), key='send', pad=(10, 10), button_color=(ui_button_b_font, ui_button_b))]], element_justification='c', justification='center'),
            sg.Text('', pad=(15, 15))],
        ########

        [sg.Text("", font=(font, 8), expand_x=True, justification='center', size=(None, 1), pad=(0, 0), text_color=main_text, background_color=ui_overall_background)],
]

window.close()

# Start a thread to update balance every 5 seconds
threading.Thread(target=update_gui_balance).start()

# Create the window
if platform.system() == 'Darwin':
    window = sg.Window('Monero Subscriptions Wallet', layout, margins=(20, 20), titlebar_icon='', titlebar_background_color=ui_overall_background, use_custom_titlebar=False, grab_anywhere=True, icon=icon)
else:
    window = sg.Window(title_bar_text, layout, margins=(20, 20), titlebar_icon='', titlebar_background_color=ui_overall_background, use_custom_titlebar=True, grab_anywhere=True, icon=icon)

# MAIN EVENT LOOP ######################################################################################################
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    elif event == 'copy_address':
        pyperclip.copy(wallet_address)  # copy to clipboard
        print(f'COPIED: {wallet_address}')

    elif event == 'add_subscription':
        # Display the "How would you like to add this subscription?" popup
        choice = sg.popup("        How would you like to add this subscription?\n", text_color=ui_sub_font, title='', custom_text=("    Manually    ", "    Paste From Merchant    "), no_titlebar=True, background_color=ui_title_bar, modal=True, grab_anywhere=True, icon=icon)
        if "From Merchant" in choice:
            add_subscription_from_merchant()
        elif "Manually" in choice:
            add_subscription_manually()

    elif event == 'send':
        try:
            withdraw_to_wallet = values['withdraw_to_wallet']
            withdraw_amount = float(values['withdraw_amount'])
            print(withdraw_to_wallet)
            print(withdraw_amount)
            send_monero(destination_address=withdraw_to_wallet, amount=withdraw_amount)

        except:
            print('failed to send')
            window['withdraw_to_wallet'].update('Error: Enter a valid wallet address and XMR amount.')

    for i, sub in enumerate(subscriptions):
        if event == f'cancel_subscription_{i}':
            print(f'TRYING TO CANCEL NUMBER: {i}')
            amount = sub["amount"]
            custom_label = sub["custom_label"]
            billing_cycle_days = sub["billing_cycle_days"]

            subscriptions = read_subscriptions()

            # Do something with the values
            print(f"Cancelled {custom_label}: ${amount}, renews in {billing_cycle_days} days")

            index = find_matching_subscription_index(subscriptions=subscriptions, custom_label=sub["custom_label"], amount=sub["amount"], billing_cycle_days=sub["billing_cycle_days"])
            if index is not None:
                subscriptions = subscriptions[:index] + subscriptions[index + 1:]
                remove_subscription(subscriptions_list=subscriptions)
                subscription_removed_popup()
                kill_everything()

window.close()
