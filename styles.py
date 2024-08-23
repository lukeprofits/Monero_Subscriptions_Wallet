import tkinter as tk
import config as cfg
from PIL import Image

import styles


def make_centered_geometry(window_resolution):
    window_resolution = window_resolution.split('x')
    window_width = int(window_resolution[0])
    window_height = int(window_resolution[1])

    # Calculate x and y coordinates for the window
    x = (SCREEN_WIDTH - window_width) / 2
    y = (SCREEN_HEIGHT - window_height) / 2

    return f'{window_width}x{window_height}+{int(x)}+{int(y)}'


# =====================
# Fonts
# =====================
font = 'Nunito Sans'


# =====================
# Font Presets
# =====================
HEADINGS_FONT_SIZE = (font, 26)
SUBHEADING_FONT_SIZE = (font, 16)
BODY_FONT_SIZE = (font, 14)


# =====================
# Hex colors
# =====================
monero_orange = '#ff6600'
ui_overall_background = '#1D1D1D'

# =====================
# Other
# =====================
def get_screen_size():
    root = tk.Tk()
    root.withdraw()  # Hide the window as it's not needed to be visible
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()  # Close the temporary window
    return screen_width, screen_height


SCREEN_WIDTH, SCREEN_HEIGHT = get_screen_size()

# =====================
# Images/Icons
# =====================
icon_orange_png = "./assets/icon_orange.png"
icon_black_png = "./assets/icon_black.png"
icon_orange_ico = "./assets/icon_orange.ico"
settings_gears_icon = "./assets/settings_icon_gears.png"
settings_sliders_icon = "./assets/settings_icon_sliders.png"
history_icon = "./assets/history_icon.png"
back_icon = "./assets/back_icon.png"
plus_icon = "./assets/plus_icon.png"
wallet_qr_code = "./assets/wallet_qr_code.png"
qr_code_overlay = "./assets/overlay.png"

icon = icon_black_png
settings_icon = settings_sliders_icon


# =====================
# Platform-Dependent Configurations
# =====================
if cfg.platform == 'Windows':
    # Views
    MAIN_VIEW_GEOMETRY = '500x215'
    PAY_VIEW_GEOMETRY = '500x215'
    SETTINGS_VIEW_GEOMETRY = '500x215'
    REVIEW_PROMPT_GEOMETRY = '500x215'
    RECEIVE_VIEW_GEOMETRY = '500x330'
    SET_CURRENCY_VIEW_GEOMETRY = '500x215'
    NODE_VIEW_GEOMETRY = '500x215'
    AMOUNT_VIEW_GEOMETRY = '500x215'
    REVIEW_REQUEST_PROMPT_VIEW_GEOMETRY = '500x215'
    WELCOME_VIEW_GEOMETRY = '500x470'
    CREATE_PAYMENT_REQUEST_VIEW_GEOMETRY = '500x255'
    COPY_PAYMENT_REQUEST_VIEW_GEOMETRY = '500x215'
    HISTORY_LARGE_VIEW_GEOMETRY = '500x325'
    HISTORY_SMALL_VIEW_GEOMETRY = '500x195'
    SUBSCRIPTIONS_LARGE_VIEW_GEOMETRY = '500x325'
    SUBSCRIPTIONS_SMALL_VIEW_GEOMETRY = '500x215'


elif cfg.platform == 'Mac':
    # Views
    MAIN_VIEW_GEOMETRY = '500x200'
    PAY_VIEW_GEOMETRY = '500x200'
    SETTINGS_VIEW_GEOMETRY = '500x205'
    REVIEW_PROMPT_GEOMETRY = '500x200'
    RECEIVE_VIEW_GEOMETRY = '500x330'
    SET_CURRENCY_VIEW_GEOMETRY = '500x215'
    NODE_VIEW_GEOMETRY = '500x200'
    AMOUNT_VIEW_GEOMETRY = '500x200'
    REVIEW_REQUEST_PROMPT_VIEW_GEOMETRY = '500x215'
    WELCOME_VIEW_GEOMETRY = '500x480'
    CREATE_PAYMENT_REQUEST_VIEW_GEOMETRY = '500x255'
    COPY_PAYMENT_REQUEST_VIEW_GEOMETRY = '500x215'
    HISTORY_LARGE_VIEW_GEOMETRY = '500x325'
    HISTORY_SMALL_VIEW_GEOMETRY = '500x195'
    SUBSCRIPTIONS_LARGE_VIEW_GEOMETRY = '500x325'
    SUBSCRIPTIONS_SMALL_VIEW_GEOMETRY = '500x200'


elif cfg.platform == 'Linux':
    # Views
    MAIN_VIEW_GEOMETRY = '500x205'
    PAY_VIEW_GEOMETRY = '500x205'
    SETTINGS_VIEW_GEOMETRY = '500x210'
    REVIEW_PROMPT_GEOMETRY = '500x205'
    RECEIVE_VIEW_GEOMETRY = '500x330'
    SET_CURRENCY_VIEW_GEOMETRY = '500x205'
    NODE_VIEW_GEOMETRY = '500x205'
    AMOUNT_VIEW_GEOMETRY = '500x205'
    REVIEW_REQUEST_PROMPT_VIEW_GEOMETRY = '500x215'
    WELCOME_VIEW_GEOMETRY = '475x515'
    CREATE_PAYMENT_REQUEST_VIEW_GEOMETRY = '500x255'
    COPY_PAYMENT_REQUEST_VIEW_GEOMETRY = '500x215'
    HISTORY_LARGE_VIEW_GEOMETRY = '500x325'
    HISTORY_SMALL_VIEW_GEOMETRY = '500x195'
    SUBSCRIPTIONS_LARGE_VIEW_GEOMETRY = '500x325'
    SUBSCRIPTIONS_SMALL_VIEW_GEOMETRY = '500x205'


else:  # Not sure if we even need this
    # Views
    MAIN_VIEW_GEOMETRY = '500x195'
    PAY_VIEW_GEOMETRY = '500x195'
    SETTINGS_VIEW_GEOMETRY = '500x205'
    REVIEW_PROMPT_GEOMETRY = '500x195'
    RECEIVE_VIEW_GEOMETRY = '500x330'
    SET_CURRENCY_VIEW_GEOMETRY = '500x215'
    NODE_VIEW_GEOMETRY = '500x215'
    AMOUNT_VIEW_GEOMETRY = '500x195'
    REVIEW_REQUEST_PROMPT_VIEW_GEOMETRY = '500x215'
    WELCOME_VIEW_GEOMETRY = '500x480'
    CREATE_PAYMENT_REQUEST_VIEW_GEOMETRY = '500x255'
    COPY_PAYMENT_REQUEST_VIEW_GEOMETRY = '500x215'
    HISTORY_LARGE_VIEW_GEOMETRY = '500x325'
    HISTORY_SMALL_VIEW_GEOMETRY = '500x195'
    SUBSCRIPTIONS_LARGE_VIEW_GEOMETRY = '500x325'
    SUBSCRIPTIONS_SMALL_VIEW_GEOMETRY = '500x195'


# =====================
# GUI Components
# =====================
def back_and_title(self, ctk, cfg, title='Enter A Title', pad_bottom=0, column_count=3):
    # Title
    label = self.add(ctk.CTkLabel(self._app, text=title, font=HEADINGS_FONT_SIZE))
    label.grid(row=0, column=0, columnspan=column_count, padx=10, pady=(10, pad_bottom), sticky="ew")

    # Back Button
    back_image = ctk.CTkImage(Image.open(styles.back_icon), size=(24, 24))
    back_button = self.add(ctk.CTkButton(self._app, image=back_image, text='', fg_color='transparent', width=35, height=30, corner_radius=7, command=self.open_main))
    back_button.grid(row=0, column=0, padx=10, pady=(10, pad_bottom), sticky="w")


# =====================
# Old (Delete if unused once project is complete)
# =====================
'''
window = ''
start_block_height = None
supported_currencies = ["USD", "XMR"]
withdraw_to_wallet = ''

# =====================
# Flags and Booleans
# =====================
rpc_is_ready = False
stop_flag = threading.Event()  # Define a flag to indicate if the threads should stop

# =====================
# Theme Variables
# =====================

# Hex Colors
ui_title_bar = '#222222'
ui_button_a = '#F96800'
ui_button_a_font = '#F0FFFF'
ui_button_b = '#716F74'
ui_button_b_font = '#FFF9FB'
ui_main_font = '#F4F6EE'
ui_sub_font = '#A7B2C7'
ui_lines = '#696563'
ui_outline = '#2E2E2E'
ui_barely_visible = '#373737'
ui_regular = '#FCFCFC'
monero_grey = '#4c4c4c'
monero_white = '#FFFFFF'
monero_grayscale_top = '#7D7D7D'
monero_grayscale_bottom = '#505050'
main_text = ui_main_font  # this lets separators be orange but text stay white
subscription_text_color = ui_sub_font
subscription_background_color = ui_overall_background  # cfg.ui_title_bar

# Set Theme
icon = 'icon.ico'

title_bar_text = 'Monero Subscriptions Wallet'
icon_png_path = "./icon.png"

#'''



