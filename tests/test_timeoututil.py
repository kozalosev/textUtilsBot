import pytest
from unittest import mock
from timeoututil import SuggestionsCounter, compute_timeout_in_minutes


@pytest.fixture
def counter() -> SuggestionsCounter:
    return SuggestionsCounter()


class TestSuggestionsCounter:
    @staticmethod
    def test_increment(counter):
        assert counter.value == 0
        for i in range(1, 10):
            assert counter.increment() == counter.value == i
        counter.reset()
        assert counter.value == 0

    @staticmethod
    def test_elapsed_time_properties():
        seconds = [15, 55, 60, 72, 125, 250]
        minutes = [0, 0, 1, 1, 2, 4]

        def seconds_generator():
            yield 0
            for n in seconds:
                yield n
                yield n

        with mock.patch("time.time", side_effect=seconds_generator()):
            counter = SuggestionsCounter()
            for expected_seconds, expected_minutes in zip(seconds, minutes):
                assert counter.seconds_elapsed == expected_seconds
                assert counter.minutes_elapsed == expected_minutes


def test_compute_timeout_in_minutes(counter):
    max_suggestions = 3
    max_suggestions_timeout = 720

    results = [720, 720, 720, 720, 1440, 2160, 2880]
    for i, expected in zip(range(1, 10), results):
        assert i == counter.increment()
        assert compute_timeout_in_minutes(counter, max_suggestions, max_suggestions_timeout) == expected
