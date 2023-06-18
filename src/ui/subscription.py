import PySimpleGUI as sg
from src.ui.common import CommonTheme
import platform
from src.subscriptions import Subscriptions
from src.ui.merchant_subscription import MerchantSubscription
from src.ui.manual_subscription import ManualSubscription
from src.wallet import Wallet
from src.thread_manager import ThreadManager
import qrcode
import clipboard

class SubscriptionUI(CommonTheme):
    def __init__(self):
        super().__init__()
        self._layout = None
        self._main_window = None
        self.wallet = Wallet()
        self.xmr_balance = None
        self.usd_balance = None
        self.unlocked_balance = None

    def refresh_balances(self):
        self.xmr_balance, self.usd_balance, self.unlocked_balance = wallet.balance()

    def layout(self):
        if not self._layout:
            self._layout = [
                [sg.Text("Monero Subscriptions Wallet", font=(self.font, 24), expand_x=True, justification='center', relief=sg.RELIEF_RIDGE, size=(None, 1), pad=(0, 0), text_color=self.main_text, background_color=self.ui_overall_background)],
                [sg.Text("Subscriptions will be paid automatically if the wallet remains open", font=("Helvetica", 10), expand_x=True, justification='center', background_color=self.ui_overall_background, pad=(0, 0))],
                [sg.Text("", font=(self.font, 8))],
                    [
                        sg.Column(
                            [
                                ########
                                [sg.Text(f'        Balance:  ${self.usd_balance} USD', size=(25, 1), font=(self.font, 18), key='wallet_balance_in_usd', text_color=self.ui_sub_font, background_color=self.ui_overall_background)],
                                [sg.Text(f'        XMR: {self.xmr_balance}', size=(25, 1), font=(self.font, 18), key='wallet_balance_in_xmr', background_color=self.ui_overall_background)],
                                ########

                                ########
                                [self.frame()],
                                ########

                            ], element_justification='center', expand_x=True, expand_y=True
                        ),
                        sg.VerticalSeparator(pad=(0, 10)),
                        sg.Column(
                            [

                                ########
                                [sg.Text('Deposit XMR:', size=(20, 1), font=(self.font, 18), justification='center', text_color=self.ui_sub_font, background_color=self.ui_overall_background)],
                                [sg.Column([
                                    [sg.Image(self.wallet.generate_qr(), size=(147, 147), key='qr_code', pad=(10, 0))],  # Placeholder for the QR code image
                                    [sg.Button("Copy Address", size=(16, 1), key='copy_address', pad=(10, 10))]],
                                    element_justification='center', pad=(0, 0))],
                                ########

                            ], expand_x=True, expand_y=True, element_justification='c'
                        )
                    ],
                    [sg.Text("", font=(self.font, 8), expand_x=True, justification='center', size=(None, 1), pad=(0, 0), text_color=self.main_text, background_color=self.ui_overall_background)],

                    ########
                    [sg.Column([
                        [sg.Text(f'      Send XMR:', size=(12, 1), font=(self.font, 14), pad=(10, 10), text_color=self.ui_sub_font, background_color=self.ui_overall_background),
                        sg.InputText(default_text='[ Enter a wallet address ]', key='withdraw_to_wallet', pad=(10, 10), justification='center', size=(46, 1)),
                        sg.InputText(default_text=' [ Enter an amount ]', key='withdraw_amount', pad=(10, 10), justification='center', size=(20, 1)),
                        sg.Button("Send", size=(8, 1), key='send', pad=(10, 10), button_color=(self.ui_button_b_font, self.ui_button_b))]], element_justification='c', justification='center'),
                        sg.Text('', pad=(15, 15))],
                    ########

                    [sg.Text("", font=(self.font, 8), expand_x=True, justification='center', size=(None, 1), pad=(0, 0), text_color=self.main_text, background_color=self.ui_overall_background)],
            ]
        return self._layout

    def rows(self, subscriptions):
        result = []

        for i, sub in enumerate(subscriptions):
            amount = sub.amount
            custom_label = sub.custom_label
            renews_in = sub.billing_cycle_days
            currency = sub.currency

            payment_is_due, payment_date = sub.determine_if_a_payment_is_due()  # hopefully this does not make booting slow

            if not payment_is_due and payment_date:
                days = seuf.check_date_for_how_many_days_until_payment_needed(date=payment_date, number_of_days=renews_in)
                renews_in = round(days)

            if currency == 'USD':
                currency_indicator_left = '$'
                currency_indicator_right = ' USD'

            elif currency == 'XMR':
                currency_indicator_left = ''
                currency_indicator_right = ' XMR'

            else:
                currency_indicator_left = ''
                currency_indicator_right = currency
            # breakpoint()
            row = [
                sg.Text(f'    {currency_indicator_left}{amount}{currency_indicator_right}', justification='left', size=(12, 1), text_color=self.subscription_text_color, background_color=self.subscription_background_color),
                sg.Column([[sg.Text((custom_label + ''), justification='center', size=(None, 1), text_color=self.subscription_text_color, background_color=self.subscription_background_color)]], expand_x=True),
                sg.Text(f'Renews in {renews_in} day(s)', justification='right', size=(16, 1), text_color=self.subscription_text_color, background_color=self.subscription_background_color),
                sg.Button("Cancel", size=(7, 1), key=f'cancel_subscription_{i}', button_color=(self.ui_regular, self.ui_barely_visible)),
            ]
            result.append(row)

        return result


    def inner_layout(self, subscriptions):
        subscription_rows = self.rows(subscriptions)
        return [*subscription_rows, [sg.Column([[sg.Button("Add New Subscription", size=(40, 1), key='add_subscription', pad=(10, 10))]], expand_x=True, element_justification='center')]]

    def column(self):
        return sg.Column(self.inner_layout(Subscriptions().all()), key='subscriptions_column', pad=(10, 10))

    def frame(self):
        return sg.Frame('My Subscriptions', layout=[[self.column()]], key='subscriptions_frame', element_justification='center', pad=(10, 10), background_color=self.subscription_background_color)

    def main_window(self):
        if not self._main_window:
            if platform.system() == 'Darwin':
                self._main_window = sg.Window('Monero Subscriptions Wallet', self.layout(), margins=(20, 20), titlebar_icon='', titlebar_background_color=self.ui_overall_background, use_custom_titlebar=False, grab_anywhere=True, icon="./icon.png", finalize=True)
            elif platform.system() == 'Linux':
                self._main_window = sg.Window('Monero Subscriptions Wallet', self.layout(), margins=(20, 20), titlebar_icon='', titlebar_background_color=self.ui_overall_background, use_custom_titlebar=False, grab_anywhere=True, icon="./icon.png", finalize=True)
            else:
                self._main_window = sg.Window(self.title_bar_text, self.layout(), margins=(20, 20), titlebar_icon='', titlebar_background_color=self.ui_overall_background, use_custom_titlebar=True, grab_anywhere=True, icon=self.icon, finalize=True)
        return self._main_window

    def event_loop(self):
        while True:
            event, values = self.main_window().read()

            # if event == tray.key:
            #     sg.cprint(f'System Tray Event = ', values[event], c='white on red')
            #     event = values[event]

            if event == sg.WIN_CLOSED:
                break

            elif event == 'copy_address':
                clipboard.copy(self.wallet.address())
                print(f'COPIED: {self.wallet.address()}')

            elif event == 'add_subscription':
                # Display the "How would you like to add this subscription?" popup
                choice = sg.popup("        How would you like to add this subscription?\n", text_color=self.ui_sub_font, title='', custom_text=("    Manually    ", "    Paste From Merchant    "), no_titlebar=True, background_color=self.ui_title_bar, modal=True, grab_anywhere=True, icon=self.icon)
                if "From Merchant" in choice:
                    MerchantSubscription().main_window()
                elif "Manually" in choice:
                    ManualSubscription().main_window()

            elif event == 'send':
                try:
                    withdraw_to_wallet = values['withdraw_to_wallet']
                    if values['withdraw_amount'] == '':
                        withdraw_amount = None
                    else:
                        withdraw_amount = float(values['withdraw_amount'])
                    print(withdraw_to_wallet)
                    print(withdraw_amount)
                    if withdraw_amount == None:
                        choice = sg.popup(f"Are you sure you want to send all your XMR to this address?\n", text_color=self.ui_sub_font, title='', custom_text=("    Yes, I am sure!    ", "    No, CANCEL!    "), no_titlebar=True, background_color=self.ui_title_bar, modal=True, grab_anywhere=True, icon=self.icon)
                        if "No, CANCEL!" in choice:
                            print("Cancelled wallet sweep!")
                            pass
                        elif "Yes, I am sure!" in choice:
                            Wallet().send(address=withdraw_to_wallet, amount=self.unlocked_balance)
                            print("The wallet has been swept!")
                    else:
                        Wallet().send(address=withdraw_to_wallet, amount=withdraw_amount)

                except Exception as e:
                    print(e)
                    print('failed to send')
                    self.main_window()['withdraw_to_wallet'].update('Error: Enter a valid wallet address and XMR amount.')

            if event in ('Show Window', sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED):
                self.main_window().un_hide()
                self.main_window().bring_to_front()

            subscriptions = Subscriptions()

            for i, sub in enumerate(subscriptions.all()):
                if event == f'cancel_subscription_{i}':
                    print(f'TRYING TO CANCEL NUMBER: {i}')
                    amount = sub.amount
                    custom_label = sub.custom_label
                    billing_cycle_days = sub.billing_cycle_days

                    # Do something with the values
                    print(f"Cancelled {custom_label}: ${amount}, renews in {billing_cycle_days} days")
                    subscription = subscriptions.find_subscription(custom_label=custom_label, amount=amount, billing_cycle_days=billing_cycle_days)
                    if subscription is not None:
                        subscriptions.remove_subscription(subscription)
                        subscriptions.write_subscriptions()
                        self.refresh_gui() # recreate the window to refresh the GUI

    def update_balance(self):
        while not ThreadManager.stop_flag().is_set():
            try:
                # Update the GUI with the new balance info
                if not self.usd_balance == '---.--':
                    self.main_window()['wallet_balance_in_usd'].update(f'        Balance:  ${self.usd_balance} USD')

                self.main_window()['wallet_balance_in_xmr'].update(f'        XMR: {self.xmr_balance:.12f}')

                # Wait before updating again
                time.sleep(5)

            except Exception as e:
                print(f'Exception in thread "update_gui_balance: {e}"')

    def refresh_gui(self):
        self.main_window().close()
        self._main_window = None # recreate the window to refresh the GUI
        self.main_window()
