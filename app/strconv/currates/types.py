import datetime
from dataclasses import dataclass
from typing import Callable, Any, Dict, Optional

__all__ = ['StatusChecker', 'RatesExtractor', 'DateExtractor', 'DataSource', 'ExchangeRates']

StatusChecker = Callable[[Dict[str, Any]], bool]
RatesExtractor = Callable[[Dict[str, Any]], Dict[str, float]]
DateExtractor = Callable[[Dict[str, float]], datetime.date]


@dataclass
class DataSource:
    name: str
    url: str
    status_checker: StatusChecker
    rates_extractor: RatesExtractor
    date_extractor: DateExtractor
    headers: Optional[Dict[str, str]] = None    # if API_KEY is not in URL


@dataclass
class ExchangeRates:
    """Wrapper around the rates fetched from one source"""
    source_name: str
    date: datetime.date
    rates: Dict[str, float]
