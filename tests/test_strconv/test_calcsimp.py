import pytest
from pathlib import Path
from strconv import currates
from strconv.calcsimp import SingleExpressionCalculator

from tests.test_currates.test_fiat import mock_source, mock_source_json


@pytest.fixture
def calc(tmp_path: Path, requests_mock) -> SingleExpressionCalculator:
    currates._mock_database(str(tmp_path / 'currates.db'))
    requests_mock.get(mock_source.url, text=mock_source_json)
    currates.update_rates([mock_source])
    return SingleExpressionCalculator()


def test_can_process(calc):
    assert not calc.can_process("foo bar")
    assert not calc.can_process("{{2*2}}")
    assert calc.can_process("2*2")
    assert calc.can_process("2+2*2 EUR to USD")
    assert calc.can_process("10 USD")
    assert calc.can_process("EUR")
    assert calc.can_process("10 dollars")
    assert calc.can_process("euro")


@pytest.mark.parametrize("expr,res", [("2*2", "4"),
                                      ("2+2*2 EUR to USD", "6.40 USD"),
                                      ("10 USD", "732.01 RUB"),
                                      ("EUR", "78.10 RUB"),
                                      ("10 dollars", "732.01 RUB"),
                                      ("euro", "78.10 RUB")])
def test_process(calc, expr, res):
    assert calc.process(expr, lang_code="ru") == res
