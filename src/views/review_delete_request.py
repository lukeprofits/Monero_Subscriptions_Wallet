import customtkinter as ctk
import monero_usd_price
from src.interfaces.view import View
from src.all_subscriptions import AllSubscriptions
from src.subscription import Subscription
import config as cfg
import clipboard
import monerorequest
from datetime import datetime


class ReviewDeleteRequestView(View):
    def build(self):
        pass

    # STILL WORKING HERE