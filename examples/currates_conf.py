import datetime
from strconv.util.currates import CurrExRatesSrc

__EXCHANGE_RATE_API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXX"

EXCHANGE_RATE_SOURCES = [
    CurrExRatesSrc('api.exchangerate.host', 'https://api.exchangerate.host/latest?base=USD', 'success', 'rates',
                   lambda json: datetime.date.fromisoformat(json['date'])),
    CurrExRatesSrc('exchangerate-api.com', f"https://v6.exchangerate-api.com/v6/{__EXCHANGE_RATE_API_KEY}/latest/USD",
                   'result', 'conversion_rates',
                   lambda json: datetime.date.fromtimestamp(json['time_last_update_unix'])),
]
