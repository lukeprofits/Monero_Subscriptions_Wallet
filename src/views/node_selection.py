import customtkinter as ctk
from src.interfaces.view import View
import config as cfg

class NodeSelectionView(View):
    def build(self):
        self._app.geometry(cfg.NODE_VIEW_GEOMETRY)

        # Title
        label = self.add(ctk.CTkLabel(self._app, text='Select Node'))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Back Button
        back_button = self.add(ctk.CTkButton(self._app, text=cfg.BACK_BUTTON_EMOJI, font=(cfg.font, 24), width=35, height=30, command=self.open_main))
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Documentation: https://customtkinter.tomschimansky.com/documentation/widgets/entry
        self._node_selection(cfg)

        next_button = self.add(ctk.CTkButton(self._app, text="Submit", command=self.select_node))
        next_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def select_node(self):
        node = self.node_selection.get()
        config = cfg.config_file
        config.set('rpc', 'node_url', node)
        config.write()
        self._app.switch_view('main')

    def _node_selection(self, config):
        node = ctk.StringVar(self._app, config.config_file.get('rpc', 'node_url'))
        self.node_selection = self.add(ctk.CTkEntry(self._app, textvariable=node, placeholder_text='xmr-node.cakewallet.com:18081'))
        self.node_selection.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
