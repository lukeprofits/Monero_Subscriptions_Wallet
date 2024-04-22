import customtkinter as ctk
from src.interfaces.view import View
import qrcode
import clipboard
from PIL import Image
import config as cfg


def generate_monero_qr(wallet_address=cfg.WALLET_ADDRESS):
    qr = qrcode.main.QRCode(version=1, box_size=25, border=0)
    qr.add_data("monero:" + wallet_address)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=cfg.monero_orange, back_color=cfg.ui_overall_background)
    # Save the image to a file
    filename = "wallet_qr_code.png"
    with open(filename, "wb") as f:
        qr_img.save(f)
    return filename


class ReceiveView(View):
    def build(self):
        self._app.geometry(cfg.RECEIVE_VIEW_GEOMETRY)

        # Back button and title
        cfg.back_and_title(self, ctk, cfg, title='Your Wallet:')

        # QR Code
        qr_image_name = generate_monero_qr(cfg.WALLET_ADDRESS)
        qr_image_object = ctk.CTkImage(dark_image=Image.open(qr_image_name), size=(190, 190))
        qr_image = self.add(ctk.CTkLabel(self._app, image=qr_image_object, text=''),)
        qr_image.grid(row=1, column=0, columnspan=3, padx=10, pady=(20, 15))

        copy_wallet_button = self.add(ctk.CTkButton(self._app, text="Copy Wallet Address", corner_radius=15, command=self.copy_wallet_address))
        copy_wallet_button.grid(row=2, column=0, columnspan=3, padx=165, pady=(0, 15), sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def copy_wallet_address(self):
        clipboard.copy(cfg.WALLET_ADDRESS)
        self._app.switch_view('main')
