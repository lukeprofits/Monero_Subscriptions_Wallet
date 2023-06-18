import threading
from lxml import html
from src.subscriptions import Subscriptions
from src.ui.node_picker import NodePicker
from src.wallet import Wallet
from src.rpc_server import RPCServer
from src.ui.please_wait import PleaseWait
from src.ui.subscription import SubscriptionUI
from src.thread_manager import ThreadManager
# Get subscriptions list
subscriptions = Subscriptions()

# ADD DAEMON/NODE ######################################################################################################
node_picker = NodePicker()

if not node_picker.node_picked():
    node_picker.pick_node()
    node_picker.close_window()

# START PREREQUISITES ##################################################################################################
wallet = Wallet()
rpc_server = RPCServer(wallet)
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
payments_thread = threading.Thread(target=subscriptions.send_recurring_payments)
payments_thread.start()

please_wait.close()

subscription_gui = SubscriptionUI()
window = subscription_gui.main_window()
subscription_gui.tray()
subscription_gui.event_loop()
ThreadManager.stop_flag().set()
subscription_gui.tray().close()
window.close()