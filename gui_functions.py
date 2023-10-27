import json
import qrcode
import PySimpleGUI as sg
from datetime import datetime
import platform
import monerorequest

import wallet_functions as wallet
import subscription_functions as sub
import config as cfg


# GUI LAYOUT FUNCTIONS #################################################################################################
def make_please_wait_popup():
    layout = [
        [sg.Text("Please Wait: Monero RPC Server Is Starting", key="wait_text", font=(cfg.font, 18),
                 background_color=cfg.ui_overall_background)],
        [sg.Text("                                   This may take a few minutes on first launch.", key="wait_text2",
                 font=(cfg.font, 10), background_color=cfg.ui_overall_background)]
    ]
    return layout


def make_node_window_layout():
    layout = [[sg.Column([
        [sg.Text("Add A Monero Node:", font=(cfg.font, 24), text_color=cfg.monero_orange, background_color=cfg.ui_overall_background)],
        [sg.Text("     For maximum privacy: Add your own node, or one run by someone you trust     \n", font=(cfg.font, 16), text_color=cfg.ui_sub_font, background_color=cfg.ui_overall_background)],
        [sg.Input(default_text='node.sethforprivacy.com:18089', key='custom_node', justification='center', size=(30, 2), font=(cfg.font, 18)), sg.Button('Add Node', key='add_node', font=(cfg.font, 12), size=(12, 1), button_color=(cfg.ui_button_a_font, cfg.ui_button_a))],
        [sg.Text('', font=(cfg.font, 4))],
        [sg.Text("...or add a random node (NOT RECOMMENDED)\n", font=(cfg.font, 12), text_color=cfg.ui_sub_font, background_color=cfg.ui_overall_background)],
        [sg.Button('          Add A Random Node          ', key='add_random_node', font=(cfg.font, 12), button_color=(cfg.ui_button_b_font, cfg.ui_button_b))],
        [sg.Text('')],
        [sg.Text("Random nodes pulled from: https://Monero.fail\n", font=(cfg.font, 10), text_color=cfg.monero_orange, background_color=cfg.ui_overall_background)],
        ], element_justification='c', justification='center')
    ]]

    return layout


# MAIN WINDOW ##########################################################################################################
def headline_section():
    layout = [
        [sg.Text("Monero Subscriptions Wallet", font=(cfg.font, 24), expand_x=True, justification='center',
                 relief=sg.RELIEF_RIDGE, size=(None, 1), pad=(0, 0), text_color=cfg.main_text,
                 background_color=cfg.ui_overall_background)],
        [sg.Text("Subscriptions will be paid automatically if the wallet remains open", font=(cfg.font, 10),
                 expand_x=True, justification='center', background_color=cfg.ui_overall_background, pad=(0, 0))],
        [sg.Text("", font=(cfg.font, 8))],
    ]
    return layout


def balance_section():
    layout = [
        [sg.Text(f'        Balance:  ${cfg.wallet_balance_usd} USD', size=(25, 1), font=(cfg.font, 18), key='wallet_balance_in_usd', text_color=cfg.ui_sub_font, background_color=cfg.ui_overall_background)],
        [sg.Text(f'        XMR: {cfg.wallet_balance_xmr}', size=(25, 1), font=(cfg.font, 18), key='wallet_balance_in_xmr', background_color=cfg.ui_overall_background)],
    ]
    return layout


def subscriptions_section(subscriptions):
    rows = []
    for i, sub in enumerate(subscriptions):
        amount, custom_label, renews_in, currency = sub["amount"], sub['custom_label'], sub["days_per_billing_cycle"], sub["currency"]

        payment_is_due, payment_date = wallet.determine_if_a_payment_is_due(sub)

        if not payment_is_due and payment_date:
            days = wallet.check_date_for_how_many_days_until_payment_needed(date=payment_date, number_of_days=renews_in)
            renews_in = round(days)

        currency_indicator_left, currency_indicator_right = ('$', ' USD') if currency == 'USD' else ('', f' {currency}')

        row = [
            sg.Text(f'    {currency_indicator_left}{amount}{currency_indicator_right}', justification='left',
                    size=(12, 1), text_color=cfg.subscription_text_color,
                    background_color=cfg.subscription_background_color),
            sg.Column([[sg.Text(custom_label, justification='center', size=(None, 1),
                                text_color=cfg.subscription_text_color,
                                background_color=cfg.subscription_background_color)]], expand_x=True),
            sg.Text(f'Renews in {renews_in} day(s)', justification='right', size=(16, 1),
                    text_color=cfg.subscription_text_color, background_color=cfg.subscription_background_color),
            sg.Button("Cancel", size=(7, 1), key=f'cancel_subscription_{i}',
                      button_color=(cfg.ui_regular, cfg.ui_barely_visible)),
        ]
        rows.append(row)

    add_button_layout = [[sg.Button("Add New Subscription", size=(40, 1), key='add_subscription', pad=(10, 10))]]
    add_button_column = sg.Column(add_button_layout, expand_x=True, element_justification='center')
    rows.append([add_button_column])

    subscriptions_column = sg.Column(rows, key='subscriptions_column', pad=(10, 10))
    frame = sg.Frame('My Subscriptions', layout=[[subscriptions_column]], key='subscriptions_frame',
                     element_justification='center', pad=(10, 10), background_color=cfg.subscription_background_color)

    return [[frame]]


def deposit_section():
    layout = [
        [sg.Text('Deposit XMR:', size=(20, 1), font=(cfg.font, 18), justification='center', text_color=cfg.ui_sub_font,
                 background_color=cfg.ui_overall_background)],
        [sg.Column([
            [sg.Image(generate_monero_qr(cfg.wallet_address), size=(147, 147), key='qr_code', pad=(10, 0))],
            # Placeholder for the QR code image
            [sg.Button("Copy Address", size=(16, 1), key='copy_address', pad=(10, 10))],
        ],
            element_justification='center', pad=(0, 0))],
    ]
    return layout


def send_section():
    layout = [
        [sg.Text(f'      Send XMR:', size=(12, 1), font=(cfg.font, 14), pad=(10, 10), text_color=cfg.ui_sub_font, background_color=cfg.ui_overall_background),
         sg.InputText(default_text='[ Enter a wallet address ]', key='withdraw_to_wallet', pad=(10, 10), justification='center', size=(46, 1)),
         sg.InputText(default_text=' [ Enter an amount ]', key='withdraw_amount', pad=(10, 10), justification='center', size=(20, 1)),
         sg.Button("Send", size=(8, 1), key='send', pad=(10, 10), button_color=(cfg.ui_button_b_font, cfg.ui_button_b))
         ],
    ]
    return layout


def create_main_window(subscriptions):  # Creates the main window and returns it
    # Define the window layout
    layout = [
        ######## TOP SIDE
        # Title
        *headline_section(),
        ######## END TOP SIDE
            [
                sg.Column(
                    [
                        ######## LEFT SIDE
                        # Balances
                        *balance_section(),
                        # Subscriptions
                        *subscriptions_section(subscriptions=subscriptions),
                        ######## END LEFT SIDE

                    ], element_justification='center', expand_x=True, expand_y=True
                ),

                # Middle Separator
                sg.VerticalSeparator(pad=(0, 10)),

                sg.Column(
                    [
                        ######## RIGHT SECTION
                        # Deposit QR Code
                        *deposit_section()
                        ######## END RIGHT SECTION

                    ], expand_x=True, expand_y=True, element_justification='c'
                )
            ],

            [sg.Text("", font=(cfg.font, 8), expand_x=True, justification='center', size=(None, 1), pad=(0, 0), text_color=cfg.main_text, background_color=cfg.ui_overall_background)],

            ######## BOTTOM SIDE
            [sg.Column([

                # Send Section
                *send_section(),

            ], element_justification='c', justification='center'),
                sg.Text('', pad=(15, 15))],
            ######## END BOTTOM SIDE

            [sg.Text("", font=(cfg.font, 8), expand_x=True, justification='center', size=(None, 1), pad=(0, 0), text_color=cfg.main_text, background_color=cfg.ui_overall_background)],
    ]

    if platform.system() == 'Darwin':
        return sg.Window('Monero Subscriptions Wallet', layout, margins=(20, 20), titlebar_icon='', titlebar_background_color=cfg.ui_overall_background, use_custom_titlebar=False, grab_anywhere=True, icon="./icon.png", finalize=True)
    elif platform.system() == 'Linux':
        return sg.Window('Monero Subscriptions Wallet', layout, margins=(20, 20), titlebar_icon='', titlebar_background_color=cfg.ui_overall_background, use_custom_titlebar=False, grab_anywhere=True, icon="./icon.png", finalize=True)
    else:
        return sg.Window(cfg.title_bar_text, layout, margins=(20, 20), titlebar_icon='', titlebar_background_color=cfg.ui_overall_background, use_custom_titlebar=True, grab_anywhere=True, icon=cfg.icon, finalize=True)


def merchant_subscription_layout():
    dev_sub_code = ''

    layout = [
        [sg.Column([
            [sg.Text("Paste Subscription Code Below", font=(cfg.font, 18), text_color=cfg.ui_sub_font)],
        ], justification='center', background_color=cfg.ui_title_bar)],
        [sg.Column([
            [sg.Text("")],
            [sg.Multiline(size=(60, 8), key="subscription_info", do_not_clear=False, autoscroll=False, default_text=dev_sub_code)],
            [sg.Button("    Add Subscription    ", key="add_merchant_subscription"),
             sg.Button("    Cancel    ", key="cancel_merchant_subscription",
                       button_color=(cfg.ui_regular, cfg.ui_barely_visible))]
        ], element_justification='c', justification='center')]
    ]

    return layout


def add_subscription_from_merchant():
    window = sg.Window(cfg.title_bar_text, layout=merchant_subscription_layout(), modal=True, margins=(20, 20),
                       background_color=cfg.ui_title_bar, titlebar_icon='', no_titlebar=True, use_custom_titlebar=True,
                       grab_anywhere=True, icon=cfg.icon)

    while True:
        event, values = window.read()

        # CLOSE BUTTON PRESSED
        if event == sg.WIN_CLOSED or event == "cancel_merchant_subscription":
            break

        # ADD MERCHANT SUBSCRIPTION BUTTON PRESSED
        elif event == "add_merchant_subscription":
            subscription_info = values["subscription_info"]
            subscription_info = subscription_info.strip()  # in case user added any spaces or new lines

            if len(subscription_info) < 1:
                print("Merchant code cannot be empty! Not adding.")

            else:
                # Check if the user submitted a JSON dictionary rather than a Monero Payment Request
                if '{' in subscription_info[0] and '}' in subscription_info[len(subscription_info) - 1]:
                    try:
                        subscription_json = json.loads(subscription_info)
                        review_payment_popup(subscription_json)
                    except:
                        print('JSON for subscription is not valid. Not adding.')

                else:  # Assume that the user submitted a Monero Payment Request
                    try:
                        subscription_json = monerorequest.decode_monero_payment_request(subscription_info)
                        review_payment_popup(subscription_json)
                    except:
                        print('Monero subscription code is not valid. Not adding.')
                break
            break
    window.close()


def review_payment_popup(subscription_json):
    layout = [
        [sg.Column([
            [sg.Text("     Add This Payment Request?     ", font=(cfg.font, 18), text_color=cfg.ui_sub_font)],
        ], justification='center', background_color=cfg.ui_title_bar)],

        [sg.Column([
            [sg.Text("")],
            [sg.Text(f"     {str(subscription_json['custom_label'])}:     ", font=(cfg.font, 16), background_color=cfg.ui_overall_background)],
            [sg.Text("")],
            [sg.Text(f"     {str(subscription_json['amount'])} {str(subscription_json['currency'])} worth of Monero will be sent to the merchant{' every ' + str(subscription_json['days_per_billing_cycle']) + ' days.     ' if subscription_json['number_of_payments'] > 1 or subscription_json['number_of_payments'] == 0 else '.     '}", font=(cfg.font, 14), background_color=cfg.ui_overall_background)],
            [sg.Text("")],
            [sg.Text(f"     You will be billed {'until canceled.     ' if subscription_json['number_of_payments'] == 0 else str(subscription_json['number_of_payments']) + ' time(s) in total.     '}", font=(cfg.font, 14), background_color=cfg.ui_overall_background)],
            [sg.Text("")],
            [
                sg.Button("     Confirm     ", key="yes"),
                sg.Button("     Cancel     ", key="no", button_color=(cfg.ui_regular, cfg.ui_barely_visible))
            ],
            [sg.Text("")]
        ], element_justification='c', justification='center')]
    ]

    window = sg.Window("Are you sure?", layout=layout, modal=True, margins=(20, 20), background_color=cfg.ui_title_bar,
                       titlebar_icon='', no_titlebar=True, use_custom_titlebar=True, grab_anywhere=True, icon=cfg.icon)

    while True:
        event, values = window.read()

        # NO BUTTON PRESSED (OR CLOSE BUTTON)
        if event == sg.WIN_CLOSED or event == "no":
            window.close()
            break

        # YES BUTTON PRESSED
        elif event == "yes":
            sub.add_subscription(subscription_json)
            window.close()
            break


def manual_subscription_layout():
    today = datetime.today().strftime("%Y-%m-%d")  # Placeholder to display as a suggested start date

    layout = [

        # Headline
        [sg.Column([
            [sg.Text("Enter Monero Payment Details", font=(cfg.font, 18), text_color=cfg.ui_sub_font)],
        ], justification='center', background_color=cfg.ui_title_bar)
        ],

        # Fields
        [sg.Column([
            [sg.Text("")],

            [sg.Text("Custom Name:", background_color=cfg.ui_overall_background),
             sg.Input(size=(35, 1), key="custom_label")],

            [sg.Text("Amount:", background_color=cfg.ui_overall_background),
             sg.Input(size=(15, 1), key="amount", default_text='0.00'),
             sg.Combo(cfg.supported_currencies, default_value=cfg.supported_currencies[0], key="currency")],

            [sg.Text("Billing Every:", background_color=cfg.ui_overall_background),
             sg.Input(size=(3, 1), key="days_per_billing_cycle"),
             sg.Text("Day(s)", background_color=cfg.ui_overall_background)],

            [sg.Text("Start Date (YYYY-MM-DD):", background_color=cfg.ui_overall_background),
             sg.Input(default_text=today, size=(10, 1), key="start_date")],

            [sg.Text("Total Number of Payments:", background_color=cfg.ui_overall_background),
             sg.Input(size=(3, 1), key="number_of_payments"),
             sg.Text("(For recurring until canceled, use 0)", background_color=cfg.ui_overall_background)],

            [sg.Text("Seller's Wallet:", background_color=cfg.ui_overall_background),
             sg.Input(size=(102, 1), key="sellers_wallet")],

            [sg.Text("Optional Change Indicator URL:", background_color=cfg.ui_overall_background),
             sg.Input(size=(60, 1), key="change_indicator_url"),
             sg.Text("(For advanced sellers)", background_color=cfg.ui_overall_background)],

            [sg.Text("Optional Payment ID From Seller:", background_color=cfg.ui_overall_background),
             sg.Input(size=(20, 1), key="payment_id"),
             sg.Text("(A random payment_id will be generated if left blank)", background_color=cfg.ui_overall_background)],

            [sg.Text("")],

            # Buttons
            [sg.Column([
                [
                    sg.Button("    Add Payment    ", key="add_manual_subscription"),
                    sg.Button("    Cancel    ", key="cancel_manual_subscription",
                              button_color=(cfg.ui_regular, cfg.ui_barely_visible))
                ]], justification='center', element_justification='c')]
        ], element_justification='l')]
    ]

    return layout


def add_subscription_manually():
    window = sg.Window(cfg.title_bar_text, layout=manual_subscription_layout(), modal=True, margins=(20, 20),
                       titlebar_icon='', no_titlebar=True, background_color=cfg.ui_title_bar, use_custom_titlebar=True,
                       grab_anywhere=True, icon=cfg.icon)
    # Event Loop
    while True:
        event, values = window.read()

        # CLOSE BUTTON PRESSED
        if event == sg.WIN_CLOSED or event == "cancel_manual_subscription":
            break

        # ADD MANUAL SUBSCRIPTION BUTTON PRESSED
        elif event == "add_manual_subscription":
            custom_label = values["custom_label"]
            sellers_wallet = values["sellers_wallet"]
            currency = values["currency"]
            amount = values["amount"]
            start_date = monerorequest.convert_datetime_object_to_truncated_RFC3339_timestamp_format(
                datetime_object=datetime.strptime(values["start_date"], "%Y-%m-%d"))
            days_per_billing_cycle = int(values["days_per_billing_cycle"])
            number_of_payments = int(values["number_of_payments"])
            change_indicator_url = values["change_indicator_url"]

            try:
                payment_id = values["payment_id"]
            except:
                payment_id = None

            if not payment_id:
                payment_id = monerorequest.make_random_payment_id()  # generates a random payment ID.

            subscription_info = monerorequest.make_monero_payment_request(
                custom_label=custom_label,
                sellers_wallet=sellers_wallet,
                currency=currency,
                amount=amount,
                payment_id=payment_id,
                start_date=start_date,
                days_per_billing_cycle=days_per_billing_cycle,
                number_of_payments=number_of_payments,
                change_indicator_url=change_indicator_url)

            subscription_json = monerorequest.decode_monero_payment_request(subscription_info)
            sub.add_subscription(subscription_json)

            print(custom_label)
            print(sellers_wallet)
            print(currency)
            print(amount)
            print(payment_id)
            print(start_date)
            print(days_per_billing_cycle)
            print(number_of_payments)
            print(change_indicator_url)

            print(subscription_info)

            window.close()
            cfg.window = create_main_window(cfg.subscriptions)
            break

    window.close()


# OTHER VISUALS ########################################################################################################
def generate_monero_qr(wallet_address=cfg.wallet_address):
    if monerorequest.Check.wallet(wallet_address=wallet_address, allow_standard=True, allow_integrated_address=False, allow_subaddress=False):
        # Generate the QR code
        qr = qrcode.QRCode(version=1, box_size=3, border=4)
        qr.add_data("monero:" + wallet_address)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color=cfg.monero_orange, back_color=cfg.ui_overall_background)
        # Save the image to a file
        filename = "wallet_qr_code.png"
        with open(filename, "wb") as f:
            qr_img.save(f, format="PNG")
        return filename

    else:
        print('Monero Address is not valid')
        return None


def refresh_gui():
    cfg.window.close()
    cfg.subscriptions = sub.read_subscriptions()
    cfg.window = create_main_window(cfg.subscriptions)  # recreate the window to refresh the GUI


def make_transparent():
    # Make the main window transparent
    cfg.window.TKroot.attributes('-alpha', 0.00)


def make_visible():
    # Make the main window transparent
    cfg.window.TKroot.attributes('-alpha', 1.00)
