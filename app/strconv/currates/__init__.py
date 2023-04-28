"""
Service for retrieval and storage of currency exchange rates

Fetches the rates for USD pairs from several sources once per day and save them into a file.
It has a function to calculate the coefficient for any pair and convert a value from one currency into another.
"""

import dbm
import datetime
import logging
import requests
import random
import asyncio
from functools import reduce
from typing import List, Iterable

from .types import *
from .exceptions import *

__all__ = ['update_rates', 'update_rates_async_loop', 'update_volatile_rates_async_loop', 'convert']

__db = dbm.open('app/data/currates.db', flag='c')
# It's filled in by update_rates() and is used as a cache of sources to fetch data
# in getter functions if the rates are missing for some reason.
__src_cache: List[DataSource] = []
_logger = logging.getLogger(__name__)


def update_rates(src: Iterable[DataSource]) -> None:
    """
    Makes HTTP requests to fetch currency exchange rates from remote sources

    It saves the data into the file representing a dbm database.

    As a side effect, it also saves the ``src`` list into the global ``__src_cache`` variable.
    It's a kind of crutch to make the ``convert()`` function more robust without making it
    to take the sources as an argument explicitly.

    :param src: a list of sources (see ``currates_conf.py`` for example)
    :raises ExternalServiceError: if something bad happened while executing request
    """

    src = list(src)

    global __src_cache
    if len(__src_cache) == 0:
        _logger.info("Filling the cache of currency rates sources...")
        __src_cache = src

    today = datetime.datetime.utcnow().date()
    volatile = all(x.volatile for x in src)
    if not volatile and 'date' in __db and __db['date'].decode() == str(today):
        _logger.info("The cache already has the actual currency exchange rates. Skipping...")
        return

    fetched_rates = [_fetch_rates(s) for s in src]
    today_rates = [r.rates for r in fetched_rates if r.date == today]

    if len(today_rates) != len(list(src)):
        filtered_out_src = [ExchangeRates(r.source_name, r.date, {}) for r in fetched_rates if r.date != today]
        _logger.warning(f"The following exchange rate sources were filtered out: {filtered_out_src}")

    rates = reduce(lambda x, y: x | y, today_rates, {})
    for curr, val in rates.items():
        __db[curr] = str(val)
    __db['date'] = str(today)


async def update_rates_async_loop(src: Iterable[DataSource]) -> None:
    """
    Scheduler function for the asyncio loop to update non-volatile rates

    It's used to delay iterations for 1 day and some random time (to be a good API user) on the main thread.
    """
    while True:
        _logger.info("Updating non-volatile rates in asynchronous loop...")
        update_rates(x for x in src if not x.volatile)

        # random delay from 1 to 60 seconds to be a good API user
        run_in_time = datetime.timedelta(days=1, minutes=5+random.randint(0, 5), seconds=random.randint(0, 60))
        _logger.info(f"Delay next update in: {run_in_time}")
        await asyncio.sleep(run_in_time.total_seconds())


async def update_volatile_rates_async_loop(src: Iterable[DataSource], period_in_hours: int) -> None:
    """
    Scheduler function for the asyncio loop to update volatile rates

    It's used to delay iterations for `period_in_hours` and some random time (to be a good API user) on the main thread.
    """
    while True:
        _logger.info("Updating volatile rates in asynchronous loop...")
        update_rates(x for x in src if x.volatile)

        # random delay from 1 to 60 seconds to be a good API user
        run_in_time = datetime.timedelta(hours=period_in_hours,
                                         minutes=5+random.randint(0, 5),
                                         seconds=random.randint(0, 60))
        _logger.info(f"Delay next update in: {run_in_time}")
        await asyncio.sleep(run_in_time.total_seconds())


def convert(from_curr: str, to_curr: str, val: float, lang_code: str) -> float:
    """
    Converts a value from one currency into another

    :param from_curr: source currency
    :param to_curr: destination currency
    :param val: numeric value
    :param lang_code: used for conversion '¥' into either 'yen' or 'yuan'
    :return: converted numeric value
    :raises UnsupportedCurrency: if one or both of the currencies isn't present in our data
    """
    from_curr = _ensure_not_symbol(from_curr, lang_code)
    to_curr = _ensure_not_symbol(to_curr, lang_code)
    return _get_coefficient_for(from_curr, to_curr) * val


def _fetch_rates(src: DataSource) -> ExchangeRates:
    resp = requests.get(src.url, headers=src.headers)
    if resp.status_code != 200:
        raise ExternalServiceError(f"{resp.status_code} {resp.reason}")
    resp = resp.json()
    if not src.status_checker(resp):
        raise ExternalServiceError(resp)
    return ExchangeRates(src.name, src.date_extractor(resp), src.rates_extractor(resp))


def _get_coefficient_for(from_curr: str, to_curr: str) -> float:
    if len(__db) == 0:
        _logger.warning("Currencies disappeared somewhere...")
        update_rates(__src_cache)

    if from_curr not in __db or to_curr not in __db:
        missed_currencies = [x for x in (from_curr, to_curr) if x not in __db]
        raise UnsupportedCurrency(*missed_currencies)

    from_usd_rate, to_usd_rate = float(__db[from_curr]), float(__db[to_curr])
    return to_usd_rate / from_usd_rate


def _ensure_not_symbol(curr: str, lang_code: str) -> str:
    if curr == "¥":
        if 'ja' in lang_code:
            return "JPY"
        elif 'zh' in lang_code:
            return "CNY"
        else:
            raise UnsupportedCurrency(f"{curr}:{lang_code}")
    match curr:
        case "$": return "USD"
        case "€": return "EUR"
        case "₽" | "RUR": return "RUB"
        case "£": return "GBP"
        case "₿": return "BTC"
        case "₹" | "₨" | "Rs" | "Rp": return "INR"
        case "₪": return "ILS"
    return curr


def _mock_database(temp_file_path: str):
    """Open another file as the cache. Used internally for testing purposes."""
    global __db
    __db.close()
    __db = dbm.open(temp_file_path, 'c')
