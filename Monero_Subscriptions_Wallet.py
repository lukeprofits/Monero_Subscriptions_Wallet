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
import monerorequest
import monero_usd_price
import PySimpleGUI as sg
from datetime import datetime
import platform
import clipboard

import wallet_functions as wallet
import subscription_functions as sub
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


# LOOPING THREADS ######################################################################################################
def send_recurring_payments():
    while not cfg.stop_flag.is_set():
        try:
            sub.read_subscriptions()

            print('Checking if subscriptions need to be paid.')

            for s in cfg.subscriptions:
                payment_is_due, payment_date = wallet.determine_if_a_payment_is_due(s)

                if payment_is_due:
                    sellers_wallet = s["sellers_wallet"]
                    currency = s["currency"]
                    amount = s["amount"]
                    payment_id = s["payment_id"]

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


# GUI FUNCTIONS (NOT LAYOUT) ###########################################################################################
def update_gui_balance():
    while not cfg.stop_flag.is_set():
        try:
            # Get the wallet balance info
            cfg.wallet_balance_xmr, cfg.wallet_balance_usd, cfg.xmr_unlocked_balance = wallet.get_wallet_balance()

            # Update the GUI with the new balance info
            if not cfg.wallet_balance_usd == '---.--':
                cfg.window['wallet_balance_in_usd'].update(f'        Balance:  ${cfg.wallet_balance_usd} USD')

            cfg.window['wallet_balance_in_xmr'].update(f'        XMR: {cfg.wallet_balance_xmr:.12f}')

            # Wait before updating again
            time.sleep(5)

        except Exception as e:
            print(f'Exception in thread "update_gui_balance: {e}"')


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
    cfg.window = sg.Window('Node Input', layout, keep_on_top=True, no_titlebar=True, grab_anywhere=True)

    # Event loop
    while True:
        event, values = cfg.window.read()
        if event == 'add_node':
            node = values['custom_node']

            if '://' in node:
                node = node.split('://')[1]

            print(node)

            if wallet.check_if_node_works(node):
                cfg.window['custom_node'].update(value="Success!")

                # Save the node to the file
                with open(cfg.node_filename, 'w') as f:
                    f.write(node + '\n')
                break

            else:
                cfg.window['custom_node'].update(value="Node did not respond. Try Another.")

        elif event == 'add_random_node':
            print('Adding a random node. Please wait. \nThe software will seem to be frozen until a node is found.')
            node = get_random_monero_node()
            # Save the node to the file
            with open(cfg.node_filename, 'w') as f:
                f.write(node + '\n')
            break

        if event == sg.WIN_CLOSED:
            break

    cfg.window.close()

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
cfg.window = sg.Window("Waiting", layout=gui.make_please_wait_popup(), finalize=True, keep_on_top=True, no_titlebar=True, grab_anywhere=True)

# Wait until the RPC server starts
while not cfg.rpc_is_ready:
    # Check for window events
    event, values = cfg.window.read(timeout=100)  # Read with a timeout so the window is updated
print('\n\nRPC Server has started')

cfg.wallet_address = wallet.get_wallet_address()  # Now that the RPC Server is running, get the wallet address

try:  # Now that the RPC Server is running, get the wallet balance
    cfg.wallet_balance_xmr, cfg.wallet_balance_usd, cfg.xmr_unlocked_balance = wallet.get_wallet_balance()
except:
    pass

# Get subscriptions list
cfg.subscriptions = sub.read_subscriptions()

# CREATE THE MAIN WINDOW ###############################################################################################
cfg.window.close()
cfg.window = gui.create_main_window(cfg.subscriptions)
# gui.bind_checkboxes(window=cfg.window)  # add this later if using. Just putting here as a reminder.


# START THREADS ########################################################################################################
# Continually update displayed GUI balance every 5 seconds
threading.Thread(target=update_gui_balance).start()

# Start a thread to send the payments
threading.Thread(target=send_recurring_payments).start()


# MAIN EVENT LOOP ######################################################################################################
while True:
    event, values = cfg.window.read()
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
            cfg.window['withdraw_to_wallet'].update('Error: Enter a valid wallet address and XMR amount.')

    # CANCEL SUBSCRIPTION BUTTON PRESSED
    for i, s in enumerate(cfg.subscriptions):
        if event == f'cancel_subscription_{i}':
            print(f'TRYING TO CANCEL NUMBER: {i}')
            amount = s["amount"]
            custom_label = s["custom_label"]
            days_per_billing_cycle = s["days_per_billing_cycle"]

            sub.read_subscriptions()

            # Do something with the values
            print(f"Cancelled {custom_label}: ${amount}, renews in {days_per_billing_cycle} days")

            index = sub.find_matching_subscription_index(subscriptions=cfg.subscriptions,
                                                         custom_label=s["custom_label"],
                                                         amount=s["amount"],
                                                         days_per_billing_cycle=s["days_per_billing_cycle"])
            if index is not None:
                cfg.subscriptions = cfg.subscriptions[:index] + cfg.subscriptions[index + 1:]
                sub.remove_subscription(subscriptions_list=cfg.subscriptions)
                gui.refresh_gui()  # recreate the window to refresh the GUI
                
cfg.window.close()
