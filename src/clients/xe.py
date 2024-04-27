from lxml import html
import requests

def scrape(currency_ticker):
    url = f"https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To={currency_ticker.upper()}"
    main_xpath = '//p[contains(text(), "1.00 US Dollar =")]/../p[2]'
    # Used to use: [contains(@class, "BigRate")] ...but that broke so switched to [2]

    response = requests.get(url)
    tree = html.fromstring(response.content)
    return tree.xpath(main_xpath)[0].text_content().strip().split(' ')[0].replace(',', '')
