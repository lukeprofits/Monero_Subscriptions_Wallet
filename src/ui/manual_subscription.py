from src.ui.common import CommonTheme
from datetime import datetime
import PySimpleGUI as sg
from src.subscriptions import Subscription, Subscriptions
import random

class ManualSubscription(CommonTheme):
    def __init__(self):
        super().__init__()
        self._layout = None

    def main_window(self):
        today = datetime.today().strftime("%Y-%m-%d")
        layout = [
            [sg.Column([
                [sg.Text("Enter Subscription Details", font=(self.font, 18), text_color=self.ui_sub_font)],
            ], justification='center', background_color=self.ui_title_bar)],
            [sg.Column([
                [sg.Text("")],
                [sg.Text("Custom Name:", background_color=self.ui_overall_background), sg.Input(size=(35, 1), key="custom_label")],
                [sg.Text("Amount:", background_color=self.ui_overall_background), sg.Input(size=(15, 1), key="amount", default_text='0.00'), sg.Combo(["USD", "XMR"], default_value="USD", key="currency")],
                [sg.Text("Billing Every:", background_color=self.ui_overall_background), sg.Input(size=(3, 1), key="billing_cycle_days"), sg.Text("Day(s)", background_color=self.ui_overall_background)],
                [sg.Text("Start Date (YYYY-MM-DD):", background_color=self.ui_overall_background), sg.Input(default_text=today, size=(10, 1), key="start_date")],
                [sg.Text("Seller's Wallet:", background_color=self.ui_overall_background), sg.Input(size=(102, 1), key="sellers_wallet")],
                [sg.Text("Optional Payment ID From Seller:", background_color=self.ui_overall_background), sg.Input(size=(20, 1), key="payment_id")],
                [sg.Text("")],
                [sg.Column([
                    [sg.Button("    Add Subscription    ", key="add_manual_subscription"), sg.Button("    Cancel    ", key="cancel_manual_subscription", button_color=(self.ui_regular, self.ui_barely_visible))]
                    ], justification='center', element_justification='c')]
            ], element_justification='l')]
        ]

        window = sg.Window(self.title_bar_text, layout=layout, modal=True, margins=(20, 20), titlebar_icon='', no_titlebar=True, background_color=self.ui_title_bar, use_custom_titlebar=True, grab_anywhere=True, icon=self.icon)

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED or event == "cancel_manual_subscription":
                break

            elif event == "add_manual_subscription":
                custom_label = values["custom_label"]
                amount = values["amount"]
                currency = values["currency"]
                billing_cycle_days = values["billing_cycle_days"]
                start_date = values["start_date"]
                sellers_wallet = values["sellers_wallet"]

                try:
                    payment_id = values["payment_id"]
                except:
                    payment_id = None

                if not payment_id:
                    # '0000000000000000' is the same as no payment_id, but you want to use one.
                    # (Without one, you can't make multiple payments at the same time to the same wallet address.)
                    payment_id = self.make_payment_id()  # generates a random payment ID.

                subscription = Subscription(custom_label=custom_label, amount=amount, currency=currency, billing_cycle_days=billing_cycle_days, start_date=start_date, sellers_wallet=sellers_wallet)
                subscription_info = subscription.encode()
                subscription_json = subscription.decode(subscription_info)
                subscriptions = Subscriptions()
                subscriptions.add_subscription(subscription)
                subscriptions.write_subscriptions()

                print(custom_label)
                print(amount)
                print(currency)
                print(billing_cycle_days)
                print(start_date)
                print(sellers_wallet)
                print(payment_id)
                print(subscription_info)

                window.close()
                # window = create_window(subscriptions)
                break

        window.close()
