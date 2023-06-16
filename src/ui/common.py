class CommonTheme():
	def __init__(self):
		self.ui_title_bar = '#222222'
		self.ui_overall_background = '#1D1D1D'
		self.ui_button_a = '#F96800'
		self.ui_button_a_font = '#F0FFFF'
		self.ui_button_b = '#716F74'
		self.ui_button_b_font = '#FFF9FB'
		self.ui_main_font = '#F4F6EE'
		self.ui_sub_font = '#A7B2C7'
		self.ui_lines = '#696563'
		self.ui_outline = '#2E2E2E'
		self.ui_barely_visible = '#373737'
		self.ui_regular = '#FCFCFC'
		self.monero_grey = '#4c4c4c'
		self.monero_orange = '#ff6600'
		self.monero_white = '#FFFFFF'
		self.monero_grayscale_top = '#7D7D7D'
		self.monero_grayscale_bottom = '#505050'
		self.icon = 'icon.ico'
		self.font = 'Nunito Sans'
		self.title_bar_text = ''
		self.main_text = self.ui_main_font  # this lets separators be orange but text stay white
		self.subscription_text_color = self.ui_sub_font
		self.subscription_background_color = self.ui_overall_background  # ui_title_bar

	def set_colors(self):
		sg.theme('DarkGrey2')
		sg.theme_background_color(ui_overall_background)  # MAIN BACKGROUND COLOR
		sg.theme_button_color((ui_button_a_font, ui_button_a))  # whiteish, blackish
		sg.theme_text_color(monero_orange)  # HEADING TEXT AND DIVIDERS
		sg.theme_text_element_background_color(ui_title_bar)  # Text Heading Boxes
		sg.theme_element_background_color(ui_title_bar)  # subscriptions & transactions box color
		sg.theme_element_text_color(ui_sub_font)  # My Subscriptions Text Color
		sg.theme_input_background_color(ui_title_bar)
		sg.theme_input_text_color(monero_orange)
		sg.theme_border_width(0)
		sg.theme_slider_border_width(0)