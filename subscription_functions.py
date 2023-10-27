import json
import os
import qrcode
import PySimpleGUI as sg
from datetime import datetime
import platform
import monerorequest

import wallet_functions as wallet
import gui_functions as gui
import config as cfg


def add_subscription(subscription):
    if subscription:
        cfg.subscriptions = read_subscriptions()
        cfg.subscriptions.append(subscription)
        with open(cfg.subs_file_path, "w") as file:
            json.dump(cfg.subscriptions, file, indent=2)
        gui.refresh_gui()


def read_subscriptions():
    if not os.path.exists(cfg.subs_file_path):
        return []

    with open(cfg.subs_file_path, "r") as file:
        cfg.subscriptions = json.load(file)

    # Sort subscriptions by days_per_billing_cycle
    cfg.subscriptions.sort(key=lambda x: x['days_per_billing_cycle'])

    return cfg.subscriptions


def find_matching_subscription_index(subscriptions, custom_label, amount, days_per_billing_cycle):
    for index, subscription in enumerate(subscriptions):
        if (subscription['custom_label'] == custom_label and
                subscription['amount'] == amount and
                subscription['days_per_billing_cycle'] == days_per_billing_cycle):
            return index
    return None


def remove_subscription(subscriptions_list):
    cfg.subscriptions = subscriptions_list

    with open(cfg.subs_file_path, "w") as file:
        json.dump(cfg.subscriptions, file, indent=2)
