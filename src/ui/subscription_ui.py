from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty

class SubscriptionUI(GridLayout):
    amount = StringProperty('')
    custom_label = StringProperty('')
    renewal_date = StringProperty('')

    def __init__(self, **kwargs):
        super(SubscriptionUI, self).__init__(**kwargs)
