import csv
from decimal import Decimal, ROUND_HALF_UP
from src.clients.goldback import scrape as goldback_scrape
from src.clients.xe import scrape as xe_scrape
from src.clients.rpc import RPCClient
from monero_usd_price import median_price, calculate_atomic_units_from_monero
from config import rpc

class Exchange():
    _options = None
    ROUNDING = {
        "BTC": 8,
        "LTC": 8,
        "BCH": 8,
        "ADA": 6,
        "DOGE": 8,
        "DOT": 8,  # 10, but rounded to fit well
        "ETH": 8,  # 18, but that does not fit on the window
        "LINK": 8,  # 18, but that does not fit on the window
        "UNI": 8  # 18, but that does not fit on the window
    }

    SYMBOLS = {
        "USD": "$",
        "BTC": "₿",
        "CYN": "¥",
        "EUR": "€",
        "JPY": "¥",
        "GBP": "£",
        "KRW": "₩",
        "INR": "₹",
        "CAD": "$",
        "HKD": "$",
        "AUD": "$"
    }

    DUMMY_AMOUNT = 1  # Show an amount if running in test mode without RPC

    US_EXCHANGE = 0
    XMR_AMOUNT = 0 if rpc() == 'True' else DUMMY_AMOUNT
    USD_AMOUNT = 0 if rpc() == 'True' else round(median_price() * DUMMY_AMOUNT, 2)

    @classmethod
    def convert(cls, to_sym):
        if to_sym != 'XMR':
            if to_sym == 'XGB':
                sym_value = goldback_scrape()
            else:
                sym_value = xe_scrape(to_sym)
            converted = Decimal(cls.USD_AMOUNT) * Decimal(sym_value)
        else:
            converted = Decimal(cls.XMR_AMOUNT)
        return str(cls._round(converted, to_sym))

    @classmethod
    def to_atomic_units(cls, from_sym, amount):
        if from_sym == 'XGB':
            sym_value = goldback_scrape()
        else:
            sym_value = xe_scrape(from_sym)

        usd_value = float(sym_value) * amount
        xmr_value = usd_value / float(cls.US_EXCHANGE)
        return calculate_atomic_units_from_monero(float(xmr_value))

    @classmethod
    def _round(cls, value, to_sym):
        if to_sym not in cls.ROUNDING.keys():
            final_rounded = format(value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP), ",.2f")
        else:
            rounding_spec = Decimal('1.' + ('0' * cls.ROUNDING[to_sym]))
            final_rounded = value.quantize(rounding_spec, rounding=ROUND_HALF_UP)
            final_rounded = format(final_rounded, f",.{str(cls.ROUNDING[to_sym])}f")
        return final_rounded

    @classmethod
    def display(cls, to_sym):
        symbol = cls.SYMBOLS.get(to_sym, '')
        return f'{symbol}{cls.convert(to_sym)} {to_sym.upper()}'

    @classmethod
    def options(cls):
        if cls._options is None:
            options = ["XMR", "BTC", "XGB", "XAU", "XAG", "USD", "EUR", "GBP", "CAD", "AUD", "CNY", "JPY", "KRW", "INR", "HKD", "BRL", "TWD", "CHF", "LTC", "BCH", "ADA", "DOGE", "DOT", "ETH", "LINK", "UNI"]
            with open('data/currency_codes.csv') as codes:
                reader = csv.DictReader(codes)
                for ticker in reader:
                    options.append(ticker['AlphabeticCode'])
                cls._options = options
        return cls._options

    @classmethod
    def refresh_prices(cls):
        cls.US_EXCHANGE = median_price()
        cls.XMR_AMOUNT = RPCClient().get_balance()
        cls.USD_AMOUNT = round(cls.US_EXCHANGE * cls.XMR_AMOUNT, 2)