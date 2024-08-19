import customtkinter as ctk
from src.interfaces.view import View
import qrcode
import clipboard
from PIL import Image
import config as cfg
from config import rpc
import styles
from src.wallet import Wallet

DUMMY_WALLET = '4Test5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4h4Test'


def generate_monero_qr(wallet_address):
    qr = qrcode.main.QRCode(version=1, box_size=25, border=0)
    qr.add_data("monero:" + wallet_address)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=styles.monero_orange, back_color=styles.ui_overall_background)
    # Save the image to a file
    filename = styles.wallet_qr_code
    with open(filename, "wb") as f:
        qr_img.save(f)
    return filename


class ReceiveView(View):

    def build(self):
        self._app.geometry(styles.RECEIVE_VIEW_GEOMETRY)

        # Back button and title
        styles.back_and_title(self, ctk, cfg, title='Your Wallet:', pad_bottom=0)

        # Plus Button
        #add_image = ctk.CTkImage(Image.open("plus_icon.png"), size=(24, 24))
        #add_button = self.add(ctk.CTkButton(self._app, image=add_image, text='', fg_color='transparent', width=35, height=30, corner_radius=7, command=self.open_create_payment_request))
        #add_button.grid(row=0, column=2, padx=10, pady=(10, 0), sticky="e")

        # QR Code
        qr_image_name = generate_monero_qr(Wallet().address if rpc() == 'True' else DUMMY_WALLET)
        qr_image_object = ctk.CTkImage(dark_image=Image.open(qr_image_name), size=(190, 190))
        qr_image = self.add(ctk.CTkLabel(self._app, image=qr_image_object, text=''),)
        qr_image.grid(row=1, column=0, columnspan=3, padx=10, pady=(15, 15))

        # Frame to hold buttons
        center_frame = self.add(ctk.CTkFrame(self._app, ))
        center_frame.grid(row=2, column=0, columnspan=3, padx=0, pady=(5, 15), sticky="nsew")
        center_frame.columnconfigure([0, 1, 2, 3], weight=1)

        copy_wallet_button = self.add(ctk.CTkButton(center_frame, text="Copy Wallet", corner_radius=15, command=self.copy_wallet_address))
        copy_wallet_button.grid(row=0, column=1, padx=(10, 5), pady=0, sticky="ew")

        create_payment_request_button = self.add(ctk.CTkButton(center_frame, text="Request Payment", corner_radius=15, command=self.open_create_payment_request))
        create_payment_request_button.grid(row=0, column=2, padx=(5, 10), pady=0, sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def open_create_payment_request(self):
        self._app.switch_view('create_payment_request')

    def copy_wallet_address(self):
        clipboard.copy(Wallet().address if rpc() == 'True' else DUMMY_WALLET)
        self._app.switch_view('main')
