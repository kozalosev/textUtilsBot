"""Utility functions and classes for implementations of different timeouts."""

import math
import time


__all__ = ['SuggestionsCounter', 'compute_timeout_in_minutes']


class SuggestionsCounter:
    """A simple counter that remembers the last time it was adjusted."""

    _value = 0                      # type: int
    _last_change_timestamp = 0.0    # type: float

    def __init__(self):
        self.update_timestamp()

    def increment(self) -> int:
        self._value += 1
        return self._value

    def reset(self) -> None:
        self._value = 0

    @property
    def value(self) -> int:
        return self._value

    @property
    def last_change_timestamp(self) -> float:
        return self._last_change_timestamp

    @property
    def seconds_elapsed(self) -> int:
        """:return: the number of seconds elapsed since the last change."""
        return math.floor(time.time() - self._last_change_timestamp)

    @property
    def minutes_elapsed(self) -> int:
        """:return: the number of minutes elapsed since the last change."""
        return math.floor(self.seconds_elapsed / 60)

    def update_timestamp(self) -> None:
        self._last_change_timestamp = time.time()

    def __str__(self) -> str:
        return "{class_name}(value={value}, last_change_timestamp={last_change_timestamp}, " \
               "seconds_elapsed={seconds_elapsed}, minutes_elapsed={minutes_elapsed})".format(
                    class_name=self.__class__.__name__,
                    value=self.value,
                    last_change_timestamp=self.last_change_timestamp,
                    seconds_elapsed=self.seconds_elapsed,
                    minutes_elapsed=self.minutes_elapsed
               )


def compute_timeout_in_minutes(counter: SuggestionsCounter, max_suggestions: int, max_suggestions_timeout: int) -> int:
    """
    Compute timeout applying a multiplier taking into account the value of the counter.

    Example of calculations:

    MAX_SUGGESTIONS = 3
    MAX_SUGGESTIONS_TIMEOUT = 720

    counter    multiplier    timeout_in_minutes
    -------------------------------------------
    1          1             720
    2          1             720
    3          1             720
    4          1             720
    5          2             1440
    6          3             2160
    7          4             2880
    ..         ..            ..
    """
    multiplier = counter.value - max_suggestions if counter.value > max_suggestions else 1
    return max_suggestions_timeout * multiplier
