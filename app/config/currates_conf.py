from os import getenv as env

from ..strconv.currates.currdsl import Currency, InEnglish, InRussian
from ..strconv.currates.types import DataSource
from ..strconv.currates.extractors import field, iso_date, timestamp_date

__EXCHANGE_RATE_API_KEY = env("EXCHANGE_RATE_API_KEY")
__COINMARKETCAP_API_KEY = env("COINMARKETCAP_API_KEY")

UPDATE_VOLATILE_PERIOD_IN_HOURS = env("UPDATE_VOLATILE_PERIOD_IN_HOURS")

EXCHANGE_RATE_SOURCES = [
    DataSource('api.exchangerate.host', "https://api.exchangerate.host/latest?base=USD",
               field('success'), field('rates'), iso_date('date')),
    DataSource('exchangerate-api.com', f"https://v6.exchangerate-api.com/v6/{__EXCHANGE_RATE_API_KEY}/latest/USD",
               field('result'), field('conversion_rates'), timestamp_date('time_last_update_unix')),
    DataSource('coinmarketcap.com',
               f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=500&convert=USD",
               status_checker=lambda json: json['status']['error_code'] == 0,
               rates_extractor=lambda json: {x['symbol']:(1/x['quote']['USD']['price']) for x in json['data']},
               date_extractor=iso_date('status.timestamp'),
               headers={'X-CMC_PRO_API_KEY': __COINMARKETCAP_API_KEY},
               volatile=True),
]

CURRENCIES_MAPPING = [
    Currency('RUB', 'RUR', 'rur', '₽', 'руб.', 'руб', 'р.', 'р', words=[
        InEnglish('ruble'), InRussian('рубл', ('ь', 'я', 'ей'))
    ]),
    Currency('USD', '$', words=[
        InEnglish('dollar'), InRussian('доллар', ('', 'а', 'ов'))
    ]),
    Currency('EUR', '€', words=[
        InEnglish('euro'), InRussian('евро')
    ]),
    Currency('BTC', '₿', words=[
        InEnglish('bitcoin'), InRussian('биткоин', ('', 'а', 'ов'))
    ]),
    Currency('INR', '₹', '₨', 'Rs', 'Rp'),
    Currency('GBP', '£'),
    Currency('ILS', '₪'),
]
