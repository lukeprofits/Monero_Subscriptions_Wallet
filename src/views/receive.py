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
    # Create the QR code
    qr = qrcode.main.QRCode(version=1, box_size=25, border=0)
    qr.add_data("monero:" + wallet_address)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=styles.monero_orange, back_color=styles.ui_overall_background).convert('RGBA')

    # Load the overlay image
    overlay = Image.open(styles.qr_code_overlay)

    # Calculate the size of the overlay image (scale it down)
    overlay_size = (qr_img.size[0] // 3, qr_img.size[1] // 3)  # Adjust the size as needed
    overlay = overlay.resize(overlay_size, Image.LANCZOS)

    # Calculate the position to paste the overlay (centered)
    overlay_position = (
        (qr_img.size[0] - overlay_size[0]) // 2,
        (qr_img.size[1] - overlay_size[1]) // 2
    )

    # Paste the overlay image onto the QR code
    qr_img.paste(overlay, overlay_position, overlay)

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

        # Frame to hold buttons
        center_frame = self.add(ctk.CTkFrame(self._app, fg_color='transparent'))
        center_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=0, sticky="nsew")
        center_frame.columnconfigure([0, 1], weight=1)

        # Left Frame
        left_frame = self.add(ctk.CTkFrame(center_frame, fg_color='transparent'))
        left_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        left_frame.columnconfigure([0], weight=1)

        # QR Code
        qr_image_name = generate_monero_qr(Wallet().address if rpc() == 'True' else DUMMY_WALLET)
        qr_image_object = ctk.CTkImage(dark_image=Image.open(qr_image_name), size=(190, 190))
        qr_image = self.add(ctk.CTkLabel(left_frame, image=qr_image_object, text=''), )
        qr_image.grid(row=0, column=0, padx=10, pady=10)

        copy_wallet_button = self.add(ctk.CTkButton(left_frame, text="Copy Wallet", corner_radius=15, command=self.copy_wallet_address))
        copy_wallet_button.grid(row=1, column=0, padx=40, pady=10, sticky="ew")



        # Right Frame
        right_frame = self.add(ctk.CTkFrame(center_frame, fg_color='transparent'))
        right_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        right_frame.columnconfigure([0, 1, 2, 3], weight=1)

        # Label
        get_monero = self.add(ctk.CTkLabel(right_frame, text="Get Monero:", font=styles.SUBHEADING_FONT_SIZE))
        get_monero.grid(row=0, column=0, columnspan=4, padx=10, pady=(5, 0), sticky="ew")

        # Buy Monero
        buy_monero = self.add(ctk.CTkButton(right_frame, text="Buy Monero", corner_radius=15, command=self.open_main))
        buy_monero.grid(row=1, column=0, columnspan=4, padx=40, pady=(0, 5), sticky="ew")

        # Earn Monero
        swap_monero = self.add(ctk.CTkButton(right_frame, text="Earn Monero", corner_radius=15, command=self.open_main))
        swap_monero.grid(row=2, column=0, columnspan=4, padx=40, pady=5, sticky="ew")

        # Sell Stuff For Monero
        buy_monero = self.add(ctk.CTkButton(right_frame, text="Sell for Monero", corner_radius=15, command=self.open_main))
        buy_monero.grid(row=3, column=0, columnspan=4, padx=40, pady=5, sticky="ew")

        # Swap For Monero
        swap_monero = self.add(ctk.CTkButton(right_frame, text="Swap for Monero", corner_radius=15, command=self.open_main))
        swap_monero.grid(row=4, column=0, columnspan=4, padx=40, pady=(5, 0), sticky="ew")



        # Label
        get_monero = self.add(ctk.CTkLabel(right_frame, text="Seller Tools:", font=styles.SUBHEADING_FONT_SIZE))
        get_monero.grid(row=5, column=0, columnspan=4, padx=10, pady=((15 + 2), 0), sticky="ew")  # The extra 2 is just so they line up

        # Create Payment Request
        create_payment_request_button = self.add(ctk.CTkButton(right_frame, text="Create Payment Request", corner_radius=15, command=self.open_create_payment_request))
        create_payment_request_button.grid(row=6, column=0, columnspan=4, padx=20, pady=(0, 5), sticky="ew")

        return self

    def open_main(self):
        self._app.switch_view('main')

    def open_create_payment_request(self):
        self._app.switch_view('create_payment_request')

    def copy_wallet_address(self):
        clipboard.copy(Wallet().address if rpc() == 'True' else DUMMY_WALLET)
        self._app.switch_view('main')
