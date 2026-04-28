"""Module for management of Prometheus metrics"""

from typing import Dict
from aiohttp.web import Request, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter

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


async def handler(_: Request) -> Response:
    return Response(body=generate_latest(), headers={"Content-Type": CONTENT_TYPE_LATEST})
