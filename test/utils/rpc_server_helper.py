from src.rpc_server import RPCServer
from src.wallet import Wallet

def rpc_server_test():
    wallet = Wallet('test_wallet')
    rpc_server = RPCServer(wallet)
    rpc_server.start()
    yield
    rpc_server.ready()
    rpc_server.kill()
