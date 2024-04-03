import customtkinter as ctk
from src.interfaces.view import View
from src.all_subscriptions import AllSubscriptions
from src.subscription import Subscription
import config as cfg
import clipboard
import monerorequest


def input_is_valid(input_string):
    if input_string:
        if input_is_valid_monero_wallet(input_string) or input_is_valid_monero_request(input_string):
            return True

    return False


def input_is_valid_monero_wallet(input_string):
    return monerorequest.Check.wallet(wallet_address=input_string, allow_standard=True, allow_integrated_address=True, allow_subaddress=True)


def input_is_valid_monero_request(input_string):
    if 'monero-request:' in input_string:
        # Decode it
        decoded_request = monerorequest.Decode.monero_payment_request_from_code(monero_payment_request=input_string)

        print(decoded_request)
        # Validate fields
        if monerorequest.Check.name(decoded_request["custom_label"]):
            if monerorequest.Check.wallet(decoded_request["sellers_wallet"]):
                if monerorequest.Check.amount(decoded_request["amount"]):
                    if monerorequest.Check.payment_id(decoded_request["payment_id"]):
                        if monerorequest.Check.start_date(decoded_request["start_date"]):
                            if monerorequest.Check.days_per_billing_cycle(decoded_request["days_per_billing_cycle"]):
                                if monerorequest.Check.number_of_payments(decoded_request["number_of_payments"]):
                                    if monerorequest.Check.change_indicator_url(decoded_request["change_indicator_url"]):
                                        return True

    else:
        return False


class PayView(View):
    def build(self):
        self._app.geometry(cfg.PAY_VIEW_GEOMETRY)

        # Title
        label = self.add(ctk.CTkLabel(self._app, text=' Pay To:', font=cfg.HEADINGS_FONT_SIZE))
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Back Button
        back_button = self.add(ctk.CTkButton(self._app, text=cfg.BACK_BUTTON_EMOJI, font=(cfg.font, 24), width=35, height=30, command=self.open_main))
        back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Input box
        self.input_box_for_wallet_or_request = self.add(ctk.CTkEntry(self._app, placeholder_text="Enter a monero payment request or wallet address..."))
        self.input_box_for_wallet_or_request.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Next button
        next_button = self.add(ctk.CTkButton(self._app, text="Next", command=self.next_button))
        next_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # CHECK IF WE CAN SKIP DISPLAYING THIS STEP
        clipboard_contents = clipboard.paste()
        if input_is_valid(input_string=clipboard_contents) and clipboard_contents != cfg.WALLET_ADDRESS:
            self.wallet_or_request_logic(input_string=clipboard_contents)

        return self

    def open_main(self):
        self._app.switch_view('main')

    def wallet_or_request_logic(self, input_string):
        if 'monero-request:' in input_string:
            monero_request = input_string
            # Show the details of the monero request, ask them to confirm
            subs = AllSubscriptions()
            subs.add(Subscription(**Subscription.decode(monero_request)))
            self._app.switch_view('subscriptions')
        else:
            cfg.SEND_TO_WALLET = input_string
            # Move to "how much" view
            self._app.switch_view('amount')

    def next_button(self):
        input_string = self.input_box_for_wallet_or_request.get().strip()
        if input_is_valid(input_string=input_string):
            self.wallet_or_request_logic(input_string=input_string)

        else:
            print('Not a Monero Payment Request or wallet address')


#4At3X5rvVypTofgmueN9s9QtrzdRe5BueFrskAZi17BoYbhzysozzoMFB6zWnTKdGC6AxEAbEE5czFR3hbEEJbsm4hCeX2D
#monero-request:1:H4sIAAAAAAAC/y2OX2+CMBTFv0uf1VSsirzpMBiTGQao05emlE7r2kL6B8Vl333FLLnJzfmdm3vODyCydsqCCMARHIMBoFeiLgxzVXFKbK2x08K7veO0Zop2Xu3z+AWMrSUWpGT9ScGM9bQincEN07jkQnB1wbSjgoFoAgdAOVl6p/7CDekkU9aAyON/gXnl3yBEZ2M4Y+GcIMbCvpNhQjBt8J343XdF0+1t/zgmK/ksl4tNmNspjYM0OQRb1zbt5/OEdDtr3nRxzIvT9JrdyfKWb/ni/Dg+rnUsM75RqZT1R5jJ8/Lw7r53ydqs012eFsGqj7REW1wR65uDAAZoCCdDOC8gjF4zghCewe8f/GxR8kABAAA=