import os
import json

import config as cfg


def get_subscriptions_from_file():
    if not os.path.exists(cfg.subs_file_path):
        return []

    with open(cfg.subs_file_path, "r") as file:
        cfg.subscriptions = json.load(file)

    # Sort subscriptions by days_per_billing_cycle
    cfg.subscriptions.sort(key=lambda x: x['days_per_billing_cycle'])

    return cfg.subscriptions
