from strconv.currates.types import DataSource
from strconv.currates.extractors import field, iso_date, timestamp_date

__EXCHANGE_RATE_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXX"
__COINMARKETCAP_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXX"

_COINMARKETCAP_LIMIT = 500

EXCHANGE_RATE_SOURCES = [
    DataSource('api.exchangerate.host', "https://api.exchangerate.host/latest?base=USD",
               field('success'), field('rates'), iso_date('date')),
    DataSource('exchangerate-api.com', f"https://v6.exchangerate-api.com/v6/{__EXCHANGE_RATE_API_KEY}/latest/USD",
               field('result'), field('conversion_rates'), timestamp_date('time_last_update_unix')),
    DataSource('coinmarketcap.com',
               f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit={_COINMARKETCAP_LIMIT}&convert=USD",
               status_checker=lambda json: json['status']['error_code'] == 0,
               rates_extractor=lambda json: {x['symbol']:(1/x['quote']['USD']['price']) for x in json['data']},
               date_extractor=iso_date('status.timestamp'),
               headers={'X-CMC_PRO_API_KEY': __COINMARKETCAP_API_KEY}),
]
