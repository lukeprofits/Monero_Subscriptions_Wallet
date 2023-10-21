import os
import time
import json
import gzip
import psutil
import base64
import random
import requests
import threading
import subprocess
from lxml import html
import monero_usd_price
import PySimpleGUI as sg
from datetime import datetime
import platform
import clipboard

import wallet_functions as wallet
import gui_functions as gui
import config as cfg


# OPEN STUFF FUNCTIONS #################################################################################################
def start_local_rpc_server_thread():
    if platform.system() == 'Windows':
        cmd = f'monero-wallet-rpc --wallet-file {cfg.wallet_name} --password "" --rpc-bind-port {cfg.rpc_bind_port} --disable-rpc-login --confirm-external-bind --daemon-host {host} --daemon-port {port}'
    else:
        cmd = f'{os.getcwd()}/monero-wallet-rpc --wallet-file {cfg.wallet_name} --password "" --rpc-bind-port {cfg.rpc_bind_port} --disable-rpc-login --confirm-external-bind --daemon-host {host} --daemon-port {port}'

    if cfg.start_block_height:
        command = f'{cfg.monero_wallet_cli_path} --wallet-file {os.path.join(cfg.wallet_file_path, cfg.wallet_name)} --password "" --restore-height {cfg.start_block_height} --command exit'
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
            cfg.rpc_is_ready = True
            break

        if process.poll() is not None:
            break


# CLOSE STUFF FUNCTIONS ################################################################################################
def kill_everything():
    print('\n\n Please close this terminal window and relaunch the Monero Subscriptions Wallet')

    cfg.stop_flag.set()  # Stop threads gracefully

    # Kill the program
    current_process = psutil.Process(os.getpid())  # Get the current process ID
    current_process.terminate()  # Terminate the current process and its subprocesses


def kill_monero_wallet_rpc():
    # Check which platform we are on and get the process list accordingly
    if platform.system() == 'Windows':
        process = subprocess.Popen("tasklist", stdout=subprocess.PIPE)
        rpc_path = 'monero-wallet-rpc.exe'
    else:
        process = subprocess.Popen("ps", stdout=subprocess.PIPE)
        rpc_path = 'monero-wallet-r'
    out, err = process.communicate()

    for line in out.splitlines():
        if rpc_path.encode() in line:
            if platform.system() == 'Windows': # Check if we are on Windows and get the PID accordingly
                pid = int(line.split()[1].decode("utf-8"))
            else:
                pid = int(line.split()[0].decode("utf-8"))
            os.kill(pid, 9)
            print(f"Successfully killed monero-wallet-rpc with PID {pid}")
            cfg.rpc_is_ready = False
            break

        else:
            print("monero-wallet-rpc process not found")


# OTHER RANDOM FUNCTIONS ###############################################################################################
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
            if wallet.check_if_node_works(url):
                print(f'WORKS: {url}')
                return url


def make_payment_id():
    payment_id = ''.join([random.choice('0123456789abcdef') for _ in range(16)])
    return payment_id


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


# LOOPING THREADS ######################################################################################################
def send_recurring_payments():
    while not cfg.stop_flag.is_set():
        try:
            cfg.subscriptions = read_subscriptions()

            print('Checking if subscriptions need to be paid.')

            for sub in cfg.subscriptions:
                payment_is_due, payment_date = wallet.determine_if_a_payment_is_due(sub)

                if payment_is_due:
                    sellers_wallet = sub["sellers_wallet"]
                    currency = sub["currency"]
                    amount = sub["amount"]
                    payment_id = sub["payment_id"]

                    if currency == 'USD':
                        print('SENDING USD')
                        xmr_amount = monero_usd_price.calculate_monero_from_usd(usd_amount=amount)
                        print(f'Sending {xmr_amount} XMR to {sellers_wallet} with payment ID {payment_id}')
                        wallet.send_monero(destination_address=sellers_wallet, amount=xmr_amount, payment_id=payment_id)

                    elif currency == 'XMR':
                        print('SENDING XMR')
                        print(f'Sending {amount} XMR to {sellers_wallet} with payment ID {payment_id}')
                        wallet.send_monero(destination_address=sellers_wallet, amount=amount, payment_id=payment_id)

            print('Checking subscriptions again in 1 min')

            time.sleep(60 * 1)  # run check every 1 min

        except Exception as e:
            print(f'Error in send_recurring_payments: {e}')


# GUI FUNCTIONS (NOT LAYOUT) ########################################################################################################
def refresh_gui():
    global window
    window.close()
    cfg.subscriptions = read_subscriptions()
    window = gui.create_main_window(cfg.subscriptions) # recreate the window to refresh the GUI


def make_transparent():
    # Make the main window transparent
    window.TKroot.attributes('-alpha', 0.00)


def make_visible():
    # Make the main window transparent
    window.TKroot.attributes('-alpha', 1.00)


def update_gui_balance():
    while not cfg.stop_flag.is_set():
        try:
            # Get the wallet balance info
            cfg.wallet_balance_xmr, cfg.wallet_balance_usd, cfg.xmr_unlocked_balance = wallet.get_wallet_balance()

            # Update the GUI with the new balance info
            if not cfg.wallet_balance_usd == '---.--':
                window['wallet_balance_in_usd'].update(f'        Balance:  ${cfg.wallet_balance_usd} USD')

            window['wallet_balance_in_xmr'].update(f'        XMR: {cfg.wallet_balance_xmr:.12f}')

            # Wait before updating again
            time.sleep(5)

        except Exception as e:
            print(f'Exception in thread "update_gui_balance: {e}"')


# RANDOM SUBSCRIPTION STUFF ############################################################################################
def find_matching_subscription_index(subscriptions, custom_label, amount, billing_cycle_days):
    for index, subscription in enumerate(subscriptions):
        if (subscription['custom_label'] == custom_label and
            subscription['amount'] == amount and
            subscription['billing_cycle_days'] == billing_cycle_days):
            return index
    return None


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
        if wallet.check_if_monero_wallet_address_is_valid_format(sellers_wallet):
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


def read_subscriptions():
    if not os.path.exists(cfg.subs_file_path):
        return []

    with open(cfg.subs_file_path, "r") as file:
        cfg.subscriptions = json.load(file)

    # Sort subscriptions by billing_cycle_days
    cfg.subscriptions.sort(key=lambda x: x['billing_cycle_days'])

    return cfg.subscriptions


def add_subscription(subscription):
    if subscription:
        cfg.subscriptions = read_subscriptions()
        cfg.subscriptions.append(subscription)
        with open(cfg.subs_file_path, "w") as file:
            json.dump(cfg.subscriptions, file, indent=2)
        refresh_gui()


def remove_subscription(subscriptions_list):
    cfg.subscriptions = subscriptions_list

    with open(cfg.subs_file_path, "w") as file:
        json.dump(cfg.subscriptions, file, indent=2)


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


# CHECK FUNCTIONS ######################################################################################################
def check_if_currency_is_supported(currency):
    # add more in the future as needed
    if currency == 'USD' or currency == 'XMR':
        return True
    else:
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


# SET THEME ############################################################################################################
# Start with template
sg.theme('DarkGrey2')

# Modify the colors you want to change
sg.theme_background_color(cfg.ui_overall_background)  # MAIN BACKGROUND COLOR
sg.theme_button_color((cfg.ui_button_a_font, cfg.ui_button_a))  # whiteish, blackish
sg.theme_text_color(cfg.monero_orange)  # HEADING TEXT AND DIVIDERS
sg.theme_text_element_background_color(cfg.ui_title_bar)  # Text Heading Boxes
sg.theme_element_background_color(cfg.ui_title_bar)  # subscriptions & transactions box color
sg.theme_element_text_color(cfg.ui_sub_font)  # My Subscriptions Text Color
sg.theme_input_background_color(cfg.ui_title_bar)
sg.theme_input_text_color(cfg.monero_orange)
sg.theme_border_width(0)
sg.theme_slider_border_width(0)

# START PROGRAM ########################################################################################################
# BEGIN "Add Daemon/Node" SECTION
if os.path.exists(cfg.node_filename):
    with open(cfg.node_filename, 'r') as f:
        node = f.readline().strip()  # read first line into 'node'
else:
    # welcome popup
    sg.popup(cfg.welcome_popup_text, icon=cfg.icon, no_titlebar=True, background_color=cfg.ui_overall_background, grab_anywhere=True)

    # Define the window's layout
    layout = gui.make_node_window_layout()

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

            if wallet.check_if_node_works(node):
                window['custom_node'].update(value="Success!")

                # Save the node to the file
                with open(cfg.node_filename, 'w') as f:
                    f.write(node + '\n')
                break

            else:
                window['custom_node'].update(value="Node did not respond. Try Another.")

        elif event == 'add_random_node':
            print('Adding a random node. Please wait. \nThe software will seem to be frozen until a node is found.')
            node = get_random_monero_node()
            # Save the node to the file
            with open(cfg.node_filename, 'w') as f:
                f.write(node + '\n')
            break

        if event == sg.WIN_CLOSED:
            break

    window.close()

host = node.split(':')[0]
port = node.split(':')[1]

daemon_rpc_url = f"http://{host}:{port}/json_rpc"
# END "Add Daemon/Node" SECTION


# START PREREQUISITES ##################################################################################################
# Check if wallet exists, auto-create one if it doesn't, and get block height
cfg.start_block_height = wallet.check_if_wallet_exists(daemon_rpc_url=daemon_rpc_url)

# Start Local RPC Server
kill_monero_wallet_rpc()
threading.Thread(target=start_local_rpc_server_thread).start()

# Make "Please Wait" Popup
window = sg.Window("Waiting", layout=gui.make_please_wait_popup(), finalize=True, keep_on_top=True, no_titlebar=True, grab_anywhere=True)

# Wait until the RPC server starts
while not cfg.rpc_is_ready:
    # Check for window events
    event, values = window.read(timeout=100)  # Read with a timeout so the window is updated
print('\n\nRPC Server has started')

cfg.wallet_address = wallet.get_wallet_address()  # Now that the RPC Server is running, get the wallet address

try:  # Now that the RPC Server is running, get the wallet balance
    cfg.wallet_balance_xmr, cfg.wallet_balance_usd, cfg.xmr_unlocked_balance = wallet.get_wallet_balance()
except:
    pass

# Get subscriptions list
cfg.subscriptions = read_subscriptions()

# CREATE THE MAIN WINDOW ###############################################################################################
window.close()
window = gui.create_main_window(cfg.subscriptions)
# gui.bind_checkboxes(window=window)  # add this later if using. Just putting here as a reminder.


# START THREADS ########################################################################################################
# Continually update displayed GUI balance every 5 seconds
threading.Thread(target=update_gui_balance).start()

# Start a thread to send the payments
threading.Thread(target=send_recurring_payments).start()


# MAIN EVENT LOOP ######################################################################################################
while True:
    event, values = window.read()
    print(f"Event: {event}, Values: {values}")

    # CLOSE BUTTON PRESSED
    if event == sg.WIN_CLOSED:
        break

    # COPY ADDRESS BUTTON PRESSED
    elif event == 'copy_address':
        clipboard.copy(cfg.wallet_address)
        print(f'COPIED: {cfg.wallet_address}')

    # ADD SUBSCRIPTION BUTTON PRESSED
    elif event == 'add_subscription':
        # Display the "How would you like to add this subscription?" popup
        choice = sg.popup("        How would you like to add this subscription?\n", text_color=cfg.ui_sub_font, title='', custom_text=("    Manually    ", "    Paste From Merchant    "), no_titlebar=True, background_color=cfg.ui_title_bar, modal=True, grab_anywhere=True, icon=cfg.icon)
        if "From Merchant" in choice:
            gui.add_subscription_from_merchant()
        elif "Manually" in choice:
            gui.add_subscription_manually()

    # SEND BUTTON PRESSED
    elif event == 'send':
        try:
            withdraw_to_wallet = values['withdraw_to_wallet']
            if values['withdraw_amount'] == '':
                withdraw_amount = None
            else:
                withdraw_amount = float(values['withdraw_amount'])
            print(withdraw_to_wallet)
            print(withdraw_amount)
            if withdraw_amount == None:
                choice = sg.popup(f"Are you sure you want to send all your XMR to this address?\n", text_color=cfg.ui_sub_font, title='', custom_text=("    Yes, I am sure!    ", "    No, CANCEL!    "), no_titlebar=True, background_color=cfg.ui_title_bar, modal=True, grab_anywhere=True, icon=cfg.icon)
                if "No, CANCEL!" in choice:
                    print("Cancelled wallet sweep!")
                    pass
                elif "Yes, I am sure!" in choice:
                    wallet.send_monero(destination_address=withdraw_to_wallet, amount=cfg.xmr_unlocked_balance)
                    print("The wallet has been swept!")
            else:
                wallet.send_monero(destination_address=withdraw_to_wallet, amount=withdraw_amount)

        except Exception as e:
            print(e)
            print('failed to send')
            window['withdraw_to_wallet'].update('Error: Enter a valid wallet address and XMR amount.')

    # CANCEL SUBSCRIPTION BUTTON PRESSED
    for i, sub in enumerate(cfg.subscriptions):
        if event == f'cancel_subscription_{i}':
            print(f'TRYING TO CANCEL NUMBER: {i}')
            amount = sub["amount"]
            custom_label = sub["custom_label"]
            billing_cycle_days = sub["billing_cycle_days"]

            cfg.subscriptions = read_subscriptions()

            # Do something with the values
            print(f"Cancelled {custom_label}: ${amount}, renews in {billing_cycle_days} days")

            index = find_matching_subscription_index(subscriptions=cfg.subscriptions, custom_label=sub["custom_label"], amount=sub["amount"], billing_cycle_days=sub["billing_cycle_days"])
            if index is not None:
                cfg.subscriptions = cfg.subscriptions[:index] + cfg.subscriptions[index + 1:]
                remove_subscription(subscriptions_list=cfg.subscriptions)
                refresh_gui() # recreate the window to refresh the GUI
                
window.close()
