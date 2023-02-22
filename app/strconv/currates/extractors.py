"""Extractors for DataSource config"""

import datetime
from typing import Callable, TypeVar, Any

T = TypeVar('T')
DataConverter = Callable[[Any], T]


def field(name: str) -> Callable[[dict], T]:
    """Extracts the value of a field recursively (use ``.`` as a separator)"""
    return _rec_extractor(name, lambda x: x)


def iso_date(field_name: str) -> Callable[[dict], datetime.date]:
    """Extracts a date from a field recursively (use ``.`` as a separator) stripping everything after the date part"""
    return _rec_extractor(field_name, lambda x: datetime.date.fromisoformat(x[:10]))


def timestamp_date(field_name: str) -> Callable[[dict], datetime.date]:
    """Extracts a date from a field recursively (use ``.`` as a separator)"""
    return _rec_extractor(field_name, lambda x: datetime.date.fromtimestamp(x))


def _rec_extractor(field_name: str, converter: DataConverter) -> Callable[[dict], T]:
    def extractor(data: dict) -> T:
        def rec_extractor(f_name: str, dat: dict) -> T:
            elems = f_name.split('.')
            if len(elems) == 1:
                return converter(dat[f_name])
            else:
                return rec_extractor('.'.join(elems[1:]), dat[elems[0]])
        return rec_extractor(field_name, data)
    return extractor
