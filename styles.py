import config as cfg


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
# Platform-Dependent Configurations
# =====================
if cfg.platform == 'Windows':
    BACK_BUTTON_EMOJI = '⏴'
    SETTINGS_BUTTON_EMOJI = '☰'
    # Views
    MAIN_VIEW_GEOMETRY = '500x215'
    PAY_VIEW_GEOMETRY = '500x215'
    SETTINGS_VIEW_GEOMETRY = '500x215'
    SUBSCRIPTIONS_VIEW_GEOMETRY = '500x325'
    SUBSCRIPTIONS_VIEW_NO_SUBS_GEOMETRY = '500x195'
    RECEIVE_VIEW_GEOMETRY = '500x325'
    SET_CURRENCY_VIEW_GEOMETRY = '360x165'
    NODE_VIEW_GEOMETRY = '500x215'
    AMOUNT_VIEW_GEOMETRY = '500x195'
    REVIEW_REQUEST_VIEW_GEOMETRY = '500x215'
    WELCOME_VIEW_GEOMETRY = '500x480'

elif cfg.platform == 'Mac':
    BACK_BUTTON_EMOJI = '⬅'
    SETTINGS_BUTTON_EMOJI = '⚙'
    # Views
    MAIN_VIEW_GEOMETRY = '500x200'
    PAY_VIEW_GEOMETRY = '500x200'
    SETTINGS_VIEW_GEOMETRY = '500x205'
    SUBSCRIPTIONS_VIEW_GEOMETRY = '500x325'
    SUBSCRIPTIONS_VIEW_NO_SUBS_GEOMETRY = '500x200'
    RECEIVE_VIEW_GEOMETRY = '500x325'
    SET_CURRENCY_VIEW_GEOMETRY = '360x165'
    NODE_VIEW_GEOMETRY = '500x200'
    AMOUNT_VIEW_GEOMETRY = '500x200'
    REVIEW_REQUEST_VIEW_GEOMETRY = '500x215'
    WELCOME_VIEW_GEOMETRY = '500x480'

elif cfg.platform == 'Linux':
    BACK_BUTTON_EMOJI = '⬅'
    SETTINGS_BUTTON_EMOJI = '⚙'
    # Views
    MAIN_VIEW_GEOMETRY = '500x200'
    PAY_VIEW_GEOMETRY = '500x200'
    SETTINGS_VIEW_GEOMETRY = '500x210'
    SUBSCRIPTIONS_VIEW_GEOMETRY = '500x325'
    SUBSCRIPTIONS_VIEW_NO_SUBS_GEOMETRY = '500x195'
    RECEIVE_VIEW_GEOMETRY = '500x325'
    SET_CURRENCY_VIEW_GEOMETRY = '360x165'
    NODE_VIEW_GEOMETRY = '500x215'
    AMOUNT_VIEW_GEOMETRY = '500x195'
    REVIEW_REQUEST_VIEW_GEOMETRY = '500x215'
    WELCOME_VIEW_GEOMETRY = '500x480'

else:  # Right now this is unneeded because anything not mac/windows is assumed to be linux.
    BACK_BUTTON_EMOJI = '⬅'
    SETTINGS_BUTTON_EMOJI = '⚙'
    # Views
    MAIN_VIEW_GEOMETRY = '500x195'
    PAY_VIEW_GEOMETRY = '500x195'
    SETTINGS_VIEW_GEOMETRY = '500x205'
    SUBSCRIPTIONS_VIEW_GEOMETRY = '500x325'
    SUBSCRIPTIONS_VIEW_NO_SUBS_GEOMETRY = '500x195'
    RECEIVE_VIEW_GEOMETRY = '500x325'
    SET_CURRENCY_VIEW_GEOMETRY = '360x165'
    NODE_VIEW_GEOMETRY = '500x215'
    AMOUNT_VIEW_GEOMETRY = '500x195'
    REVIEW_REQUEST_VIEW_GEOMETRY = '500x215'
    WELCOME_VIEW_GEOMETRY = '500x480'


# =====================
# GUI Components
# =====================
def back_and_title(self, ctk, cfg, title='Enter A Title', pad_bottom=0):
    # Title
    label = self.add(ctk.CTkLabel(self._app, text=title, font=HEADINGS_FONT_SIZE))
    label.grid(row=0, column=0, columnspan=3, padx=10, pady=(10, pad_bottom), sticky="ew")

    # Back Button
    back_button = self.add(ctk.CTkButton(self._app, text=BACK_BUTTON_EMOJI, font=(font, 24), width=35, height=30, command=self.open_main))
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



