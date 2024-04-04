import customtkinter as ctk
from src.interfaces.view import View
import qrcode
from PIL import Image, ImageTk

import config as cfg


def generate_monero_qr(wallet_address=cfg.WALLET_ADDRESS):
    qr = qrcode.main.QRCode(version=1, box_size=3, border=4)
    qr.add_data("monero:" + cfg.WALLET_ADDRESS)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=cfg.monero_orange, back_color=cfg.ui_overall_background)
    # Save the image to a file
    filename = "wallet_qr_code.png"
    with open(filename, "wb") as f:
        qr_img.save(f, format="PNG")
    return filename


class ReceiveView(View):
    def build(self):
        self._app.geometry(cfg.RECEIVE_VIEW_GEOMETRY)

        # Title
        label = self.add(ctk.CTkLabel(self._app, text=' Receive:'))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Back Button
        back_button = self.add(ctk.CTkButton(self._app, text=cfg.BACK_BUTTON_EMOJI, font=(cfg.font, 24), width=35, height=30, command=self.open_main))
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # QR Code
        qr_image_name = generate_monero_qr(cfg.wallet_address)
        qr_image_object = ctk.CTkImage(dark_image=Image.open(qr_image_name), size=(150, 150))
        qr_image = self.add(ctk.CTkLabel(self._app, image=qr_image_object, text=''),)
        qr_image.grid(row=1, column=0, columnspan=3, padx=10, pady=0)

        # Wallet input box
        # Documentation: https://customtkinter.tomschimansky.com/documentation/widgets/entry
        #input_box_for_wallet_or_request = self.add(ctk.CTkEntry(self._app, placeholder_text="Enter a monero payment request or wallet address..."))
        #input_box_for_wallet_or_request.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        copy_wallet_button = self.add(ctk.CTkButton(self._app, text="Copy Wallet Address", command=self.copy_wallet_address))
        copy_wallet_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def copy_wallet_address(self):
        self._app.switch_view('main')  # TODO: UPDATE THIS TO WORK!!!
