import pytest
from pathlib import Path
from strconv import currates
from strconv.calc import Calculator

from tests.test_currates.test_fiat import mock_source, mock_source_json


@pytest.fixture
def calc(tmp_path: Path, requests_mock) -> Calculator:
    currates._mock_database(str(tmp_path / 'currates.db'))
    requests_mock.get(mock_source.url, text=mock_source_json)
    currates.update_rates([mock_source])
    return Calculator()


def test_can_process(calc):
    assert not calc.can_process("foo bar")
    assert calc.can_process("{{2*2}}")
    assert calc.can_process("foo{{2+2}}bar")
    assert calc.can_process("foo {{2+2*2 EUR to USD}} bar")
    assert calc.can_process("foo {{8.5 ¥ > ₽}} bar {{10/3}} baz")
    assert calc.can_process("{{ (2+2)*2 }}")


@pytest.mark.parametrize("expr,res", [("{{2*2}}", "4"),
                                      ("{{0.0}}", "0"),
                                      ("foo{{2+2}}bar", "foo4bar"),
                                      ("foo {{2+2*2 EUR to USD}} bar", "foo 6.40 USD bar"),
                                      ("foo {{9.85 ¥ > ₽}} bar {{10/3}} baz", "foo ₽105.63 bar 3.33 baz"),
                                      ("{{7,26 / 6}}", "1.21"),
                                      ("{{ (2+2)*2 }}", "8"),
                                      ("{{ 10 долларов в рубли }}", "732.01 рублей"),
                                      ("{{ 10 долларов }}, {{ 10 евро в рубли }}", "68.26 CNY, 781.02 рублей")])
def test_process(calc, expr, res):
    assert calc.process(expr, lang_code="zh") == res
