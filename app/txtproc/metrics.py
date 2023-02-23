"""Module for management of Prometheus metrics"""

from typing import Dict
from prometheus_client import start_http_server, Counter

from .abc import TextProcessor

_COUNTER_PREFIX = "used_processor_"
_counters: Dict[str, Counter] = {}


def register(*processors: TextProcessor) -> None:
    """Registers counter metrics for all processors"""
    for proc in processors:
        _counters[proc.snake_case_name] = Counter(_COUNTER_PREFIX + proc.snake_case_name, f"{proc.name} usage")


def inc(query_id: str) -> None:
    """
    Increments the counter
    :param query_id: in format ``{index_number}:{proc_name}``
    """
    proc_name = "".join(query_id.split(':')[1:])
    _counters[proc_name].inc()


def serve(port: int) -> None:
    """Runs a WSGI server for metrics"""
    start_http_server(port)
