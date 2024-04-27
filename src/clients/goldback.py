import requests
import re
from decimal import Decimal

def scrape():
    url = 'https://www.goldback.com/exchange-rate'
    page_content = requests.get(url).text
    # Find the gb_average_exchange_rate constant's value
    usd_cost_for_one_goldback = re.search(r"gb_average_exchange_rate\s*=\s*'([\d.]+)';", page_content).group(1)
    dollar_value_in_goldbacks = Decimal(1) / Decimal(usd_cost_for_one_goldback)
    return dollar_value_in_goldbacks
