import logging
from kivy.uix.screenmanager import Screen
from src.wallet import Wallet
from src.rpc_server import RPCServer
from src.rpc_config import RPCConfig

class Loading(Screen):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(self.__module__)
        super(Loading, self).__init__(**kwargs)

    def on_pre_enter(self):
        if RPCConfig().host:
            wallet = Wallet()
            rpc_server = RPCServer(wallet)    #Have this handle waiting for the RPC server to start, perhaps even starting it
            rpc_server.start()
            self.logger.debug('In Pre-Enter')
            rpc_server.check_if_rpc_server_ready(self)

    def set_default(self, dt):
        try:
            self.parent.current = 'default'
        except AttributeError as e:
            self.logger.debug("Couldn't set default")

    def set_node_picker(self, dt):
        try:
            self.parent.current = 'node_picker'
        except AttributeError as e:
            self.logger.debug("Couldn't set node_picker")
