from kivy.utils import get_color_from_hex

class CommonTheme():
	def __init__(self):
		self.monero_orange_hex = '#ff6600'
		self.ui_overall_background_hex = '#1D1D1D'
		self.ui_title_bar = get_color_from_hex('#222222')
		self.ui_overall_background = get_color_from_hex(self.ui_overall_background_hex)
		self.ui_button_a = get_color_from_hex('#F96800')
		self.ui_button_a_font = get_color_from_hex('#F0FFFF')
		self.ui_button_b = get_color_from_hex('#716F74')
		self.ui_button_b_font = get_color_from_hex('#FFF9FB')
		self.ui_main_font = get_color_from_hex('#F4F6EE')
		self.ui_sub_font = get_color_from_hex('#A7B2C7')
		self.ui_lines = get_color_from_hex('#696563')
		self.ui_outline = get_color_from_hex('#2E2E2E')
		self.ui_barely_visible = get_color_from_hex('#373737')
		self.ui_regular = get_color_from_hex('#FCFCFC')
		self.monero_grey = get_color_from_hex('#4c4c4c')
		self.monero_orange = get_color_from_hex(self.monero_orange_hex)
		self.monero_white = get_color_from_hex('#FFFFFF')
		self.monero_grayscale_top = get_color_from_hex('#7D7D7D')
		self.monero_grayscale_bottom = get_color_from_hex('#505050')
		self.icon = 'icon.ico'
		self.font = 'Nunito Sans'
		self.title_bar_text = ''
		self.main_text = self.ui_main_font  # this lets separators be orange but text stay white
		self.subscription_text_color = self.ui_sub_font
		self.subscription_background_color = self.ui_overall_background  # ui_title_bar
		# self.set_colors()

	def set_colors(self):
		sg.theme('DarkGrey2')
		sg.theme_background_color(self.ui_overall_background)  # MAIN BACKGROUND COLOR
		sg.theme_button_color((self.ui_button_a_font, self.ui_button_a))  # whiteish, blackish
		sg.theme_text_color(self.monero_orange)  # HEADING TEXT AND DIVIDERS
		sg.theme_text_element_background_color(self.ui_title_bar)  # Text Heading Boxes
		sg.theme_element_background_color(self.ui_title_bar)  # subscriptions & transactions box color
		sg.theme_element_text_color(self.ui_sub_font)  # My Subscriptions Text Color
		sg.theme_input_background_color(self.ui_title_bar)
		sg.theme_input_text_color(self.monero_orange)
		sg.theme_border_width(0)
		sg.theme_slider_border_width(0)