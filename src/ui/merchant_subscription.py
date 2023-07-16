from src.ui.common import CommonTheme
from src.subscriptions import Subscriptions
from src.subscription import Subscription
from src.thread_manager import ThreadManager
import PySimpleGUI as sg

class MerchantSubscription(CommonTheme):
    def __init__(self):
        super().__init__()
        self._layout = None

    def main_window(self):
        #dev_sub_code = 'monero-subscription:H4sIACsJZGQC/12OXU+DMBSG/wrh2pkCAzPvYICJRhO36eZuSFvOBrEfpC3T1vjfbXfpuTrnfZ/kOT8xnbWRvGOYAIvvo3iPGQMT1XABJidQUS0FNqMU8U0Ua/Cl0t3XFQr4sjTZIVeXdzvt5OnMZ3hZ6dWrUa7fQF7N0Cr9WR7H5K6SH2RwVkvn5HNbFW4vdk/9w7oov5uSNE1OXbvJBr89Es2XwxoO6TZI6awUCGqD7m1bhwhzOYvgT9At8veELQdhurEPEPo3188NVqbrsYFApCjNFihfJEXoyMjYKM4dtZSBZ6z2TIZ+/wAVPrHVHQEAAA=='
        dev_sub_code = ''

        layout = [
            [sg.Column([
                [sg.Text("Paste Subscription Code Below", font=(self.font, 18), text_color=self.ui_sub_font)],
            ], justification='center', background_color=self.ui_title_bar)],
            [sg.Column([
                [sg.Text("")],
                [sg.Multiline(size=(60, 8), key="subscription_info", do_not_clear=False, autoscroll=False, default_text=dev_sub_code)],
                [sg.Button("    Add Subscription    ", key="add_merchant_subscription"), sg.Button("    Cancel    ", key="cancel_merchant_subscription", button_color=(self.ui_regular, self.ui_barely_visible))]
            ], element_justification='c', justification='center')]
        ]

        window = sg.Window(self.title_bar_text, layout=layout, modal=True, margins=(20, 20), background_color=self.ui_title_bar, titlebar_icon='', no_titlebar=True, use_custom_titlebar=True, grab_anywhere=True, icon=self.icon)

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == "cancel_merchant_subscription":
                break

            elif event == "add_merchant_subscription":
                subscription_info = values["subscription_info"]
                subscription_info = subscription_info.strip()  # in case user added any spaces or new lines

                if len(subscription_info) < 1:
                    print("Merchant code cannot be empty! Not adding.")

                else:
                    # Check if the user submitted a dictionary rather than a monero-subscription code
                    if '{' in subscription_info[0] and '}' in subscription_info[len(subscription_info)-1]:
                        try:
                            subscription_json = json.loads(subscription_info)
                            self.show_subscription_model(subscription_json)
                        except:
                            print('JSON for subscription is not valid. Not adding.')

                    else:  # Assume that the user submitted a monero-subscription code
                        try:
                            subscription_json = Subscription.decode(subscription_info)
                            self.show_subscription_model(subscription_json)
                        except:
                            print('Monero subscription code is not valid. Not adding.')
                    break
                break
        window.close()

    def show_subscription_model(self, subscription_json):
        layout = [[sg.Text("     Are You Sure You Want To Add This Subscription?", font=(self.font, 18), text_color=self.ui_sub_font)],
        [sg.Text(str(subscription_json['custom_label']))],
        [sg.Text("Every " + str(subscription_json['billing_cycle_days']) + " days")],
        [sg.Text(str(subscription_json['amount']) + " " + str(subscription_json['currency']) + " will be sent to the merchant")],  # str(subscription_json['sellers_wallet'])
        [sg.Button("     Yes     ", key="yes"), sg.Button("     No     ", key="no")]]
        window = sg.Window("Are you sure?", layout=layout, modal=True, margins=(20, 20), background_color=self.ui_title_bar, titlebar_icon='', no_titlebar=True, use_custom_titlebar=True, grab_anywhere=True, icon=self.icon)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "no":
                window.close()
                break
            elif event == "yes":
                subs = Subscriptions()
                subs.add_subscription(Subscription(**subscription_json))
                subs.write_subscriptions()
                ThreadManager.update_subscriptions().set()
                window.close()
                break