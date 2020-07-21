import json

import requests


def get_course(currency):
    global_request = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
    global_data = json.loads(global_request.text)['Valute']
    return global_data[currency]['Value']


def convert(exchange_currency, value):
    return float(value / float(get_course(exchange_currency)))


currencies = {
    "USA Dollar": "USD",
    "Euro": "EUR",
    "Canadian Dollar": "CAD"
}

exchange_currencies = {
    "dollar": "USD",
    "euro": "EUR",
    "cdollar": "CAD"
}
