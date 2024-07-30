import os
from src.rpc_server import RPCServer
from src.wallet import Wallet

def rpc_server_test(wallet_name='test_wallet'):
    wallet = Wallet('test_wallet')
    os.environ['MONERO_SUBSCRIPTION_WALLET_STAGENET'] = 'true'
    rpc_server = RPCServer(wallet)
    rpc_server.start()
    yield
    rpc_server.ready()
    rpc_server.kill()
