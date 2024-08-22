import customtkinter as ctk
from src.interfaces.view import View
import config as cfg
import styles


def center_string(s):
    # Trim the string to 50 characters if it's longer
    trimmed_string = s[:50]

    # Center the string within 50 characters, padding with spaces
    centered_string = trimmed_string.center(50)

    return centered_string


class HistoryView(View):
    def build(self):
        if len(cfg.transactions) > 1:
            self._app.geometry(styles.SUBSCRIPTIONS_VIEW_GEOMETRY)
        else:
            self._app.geometry(styles.REVIEW_PROMPT_GEOMETRY)

        # Back button and title
        styles.back_and_title(self, ctk, cfg, title='Transaction History:', pad_bottom=20)

        # Plus Button
        #add_image = ctk.CTkImage(Image.open(styles.plus_icon), size=(24, 24))
        #add_button = self.add(ctk.CTkButton(self._app, image=add_image, text='', fg_color='transparent', width=35, height=30, corner_radius=7, command=self.add_subscription))
        #add_button.grid(row=0, column=2, padx=10, pady=(10, 20), sticky="e")

        self._app.grid_rowconfigure(1, weight=1)  # Changes this globally. Set back when closing view.

        self.transactions_frame = self.add(TransactionsScrollableFrame(master=self._app, corner_radius=0, fg_color="transparent"))

        return self

    def open_main(self):
        self._app.switch_view('main')

    def destroy(self):
        self._app.grid_rowconfigure(1, weight=0)
        self.transactions_frame._parent_frame.destroy()
        super().destroy()


class TransactionsScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid(row=1, column=0, columnspan=3, sticky='nsew')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        if cfg.transactions:
            for i, tx in enumerate(cfg.transactions):
                self._add_tx(tx, i)

        else:
            no_tx_text = ctk.CTkLabel(self, text="     No transactions yet.", )
            no_tx_text.pack(padx=10, pady=(50, 0))

    def open_main(self):
        self.master.master.master.switch_view('main')

    def _add_tx(self, tx, row):
        TransactionFrame(self, tx, row)


class TransactionFrame(ctk.CTkFrame):
    def __init__(self, master, tx, row, **kwargs):
        super().__init__(master, **kwargs)

        # Padding and stuff for each TransactionFrame
        self.grid(row=row, column=1, columnspan=3, sticky="nsew", padx=10, pady=(0, 10))

        symbol = "+" if tx["direction"] == "in" else "-"
        tx_info_text = f"{symbol}{tx["amount"]} {center_string(tx["payment_id"])} {tx["date"]}"
        self.tx_info = ctk.CTkLabel(self, text=tx_info_text, font=styles.SUBHEADING_FONT_SIZE)
        self.tx_info.grid(row=0, column=0, pady=0, sticky="ns")

        # Center the widgets within each column
        self.columnconfigure(0, weight=1)
