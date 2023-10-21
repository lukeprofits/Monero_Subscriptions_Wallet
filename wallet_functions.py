import os
import json
import requests
import subprocess
import monero_usd_price
from datetime import datetime

import config as cfg


# CHECK FUNCTIONS ######################################################################################################
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


def check_if_wallet_exists(daemon_rpc_url):
    if not os.path.isfile(f"{cfg.wallet_name}.keys") or not os.path.isfile(cfg.wallet_name):
        # If either file doesn't exist
        start_block_height = get_current_block_height(daemon_rpc_url=daemon_rpc_url)
        create_wallet(wallet_name=cfg.wallet_name)
        return start_block_height

    else:
        # If both files exist, do nothing
        print('Wallet exists already.')
        return None


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


# ACTION FUNCTIONS #####################################################################################################
def send_monero(destination_address, amount, payment_id=None):
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

        response = requests.post(cfg.local_rpc_url, headers=headers, data=json.dumps(payload), auth=(cfg.rpc_username, cfg.rpc_password))
        response.raise_for_status()
        result = response.json().get("result")

        print('Sent Monero')

        if result is None:
            print('Failed to send Monero transaction')

    else:
        print('Wallet is not a valid monero wallet address.')


def make_integrated_address(payment_id, merchant_public_wallet_address):
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

    response = requests.post(f"{cfg.local_rpc_url}", headers=headers, data=json.dumps(data))
    result = response.json()

    if 'error' in result:
        print('Error:', result['error']['message'])

    else:
        integrated_address = result['result']['integrated_address']
        return integrated_address


def create_wallet(wallet_name=cfg.wallet_name):  # Using CLI Wallet
    # Remove existing wallet if present
    try:
        os.remove(wallet_name)
    except:
        pass

    try:
        os.remove(f'{wallet_name}.keys')
    except:
        pass

    command = f"{cfg.monero_wallet_cli_path} --generate-new-wallet {os.path.join(cfg.wallet_file_path, wallet_name)} --mnemonic-language English --command exit"
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
        cfg.wallet_address = output_text.split('Generated new wallet: ')[1].split('View key: ')[0].strip()
        view_key = output_text.split('View key: ')[1].split('*********************')[0].strip()
        seed = output_text.split(' of your immediate control.')[1].split('********')[0].strip().replace('\n', '')
        print(f'wallet_address: {cfg.wallet_address}')
        print(f'view_key: {view_key}')
        print(f'seed: {seed}')

        with open(file=f'{wallet_name}_seed.txt', mode='a', encoding='utf-8') as f:
            f.write(f'Wallet Address:\n{cfg.wallet_address}\nView Key:\n{view_key}\nSeed:\n{seed}\n\nThe above wallet should not be your main source of funds. This is ONLY to be a side account for paying monthly subscriptions. If anyone gets access to this seed, they can steal all your funds. Please use responsibly.\n\n\n\n')

        return seed, cfg.wallet_address, view_key
    else:
        print(stderr)


def get_current_block_height(daemon_rpc_url):
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
    headers = {"content-type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": "get_balance"
    }

    try:
        # get balance
        response = requests.post(cfg.local_rpc_url, headers=headers, data=json.dumps(payload), auth=(cfg.rpc_username, cfg.rpc_password))
        response.raise_for_status()
        result = response.json().get("result")

        if result is None:
            raise ValueError("Failed to get wallet balance")

        xmr_balance = monero_usd_price.calculate_monero_from_atomic_units(atomic_units=result["balance"])
        cfg.xmr_unlocked_balance = monero_usd_price.calculate_monero_from_atomic_units(atomic_units=result["unlocked_balance"])

        #print(cfg.xmr_unlocked_balance)

        try:
            usd_balance = format(monero_usd_price.calculate_usd_from_monero(float(xmr_balance)), ".2f")
        except:
            usd_balance = '---.--'

        #print(usd_balance)

        return xmr_balance, usd_balance, cfg.xmr_unlocked_balance

    except Exception as e:
        print(f'get_wallet_balance error: {e}')
        return '--.------------', '---.--'


def get_wallet_address():
    headers = {"content-type": "application/json"}
    payload = {
        "jsonrpc": "2.0",
        "id": "0",
        "method": "get_address"
    }

    response = requests.post(cfg.local_rpc_url, headers=headers, data=json.dumps(payload), auth=(cfg.rpc_username, cfg.rpc_password))
    response.raise_for_status()
    result = response.json().get("result")

    if result is None:
        raise ValueError("Failed to get wallet address")

    address = result["address"]
    print(address)
    return address


def determine_if_a_payment_is_due(subscription):
    try:  # Get all outgoing transfers from the wallet
        headers = {"Content-Type": "application/json"}
        data = {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_transfers",
            "params": {"out": True},
        }

        # Get outgoing payments
        response = requests.post(cfg.local_rpc_url, headers=headers, data=json.dumps(data))
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

