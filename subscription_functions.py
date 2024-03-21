import os
import json

import config as cfg

'''
def get_subscriptions_from_file():
    SUBS_FILE_PATH = cfg.SUBS_FILE_PATH

    if not os.path.exists(SUBS_FILE_PATH):
        return []

    with open(SUBS_FILE_PATH, "r") as file:
        cfg.subscriptions = json.load(file)

    # Sort subscriptions by days_per_billing_cycle
    cfg.subscriptions.sort(key=lambda x: x['days_per_billing_cycle'])

    return cfg.subscriptions
'''