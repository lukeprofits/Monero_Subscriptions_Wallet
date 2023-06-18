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
import subprocess
from lxml import html
import monero_usd_price
import PySimpleGUI as sg
from datetime import datetime
import platform
import clipboard
from psgtray import SystemTray
from src.ui.node_picker import NodePicker
from src.subscriptions import Subscriptions
from src.wallet import Wallet
from src.rpc_server import RPCServer
from src.ui.please_wait import PleaseWait
from src.ui.subscription import SubscriptionUI
from src.rpc_config import RPCConfig
from src.thread_manager import ThreadManager
# OVERALL FUNCTIONS ####################################################################################################
def kill_everything():
    global stop_flag

    print('\n\n Please close this terminal window and relaunch the Monero Subscriptions Wallet')

    stop_flag.set()  # Stop threads gracefully

    # Kill the program
    current_process = psutil.Process(os.getpid())  # Get the current process ID
    current_process.terminate()  # Terminate the current process and its subprocesses

def make_transparent():
    # Make the main window transparent
    window.TKroot.attributes('-alpha', 0.00)


def make_visible():
    # Make the main window transparent
    window.TKroot.attributes('-alpha', 1.00)

def build_system_tray(window):
    menu = ['', ['Show Window', 'Hide Window', '---', '!Disabled Item', 'Change Icon', ['Happy', 'Sad', 'Plain'], 'Exit']]
    tooltip = 'Tooltip'
    tray = SystemTray(menu, single_click_events=False, window=window, tooltip=tooltip, icon=sg.DEFAULT_BASE64_ICON)
    # tray.show_message('System Tray', 'System Tray Icon Started!')
    return tray

# # THEME VARIABLES ######################################################################################################

stop_flag = ThreadManager.stop_flag()  # Define a flag to indicate if the threads should stop

# Get subscriptions list
subscriptions = Subscriptions()

# ADD DAEMON/NODE ######################################################################################################
node_filename = "node_to_use.txt"

node_picker = NodePicker()

if not node_picker.node_picked():
    node_picker.pick_node()
    node_picker.close_window()

node = node_picker.picked_node()

config = RPCConfig()

# START PREREQUISITES ##################################################################################################
wallet = Wallet()
rpc_server = RPCServer(wallet, config)
rpc_server.start()
wallet.create()

please_wait = PleaseWait()
please_wait.open()

while not rpc_server.rpc_is_ready:
    # Check for window events
    event, values = please_wait.update()  # Read with a timeout so the window is updated

print('\n\nRPC Server has started')

wallet_balance_xmr = '--.------------'
wallet_balance_usd = '---.--'
wallet_address = wallet.address()

try:
    wallet_balance_xmr, wallet_balance_usd, xmr_unlocked_balance = wallet.balance()
except:
    pass

# Start a thread to send the payments
threading.Thread(target=subscriptions.send_recurring_payments).start()

please_wait.close()

subscription_gui = SubscriptionUI()
window = subscription_gui.main_window()
subscription_gui.event_loop()
tray = build_system_tray(window)
