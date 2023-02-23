import datetime
from strconv import currates
from strconv.currates.extractors import field, iso_date
from pathlib import Path

mock_source = currates.DataSource('mock_source', 'http://localhost/fiat',
                                  field('success'), field('rates'), iso_date('date'))
mock_rub = 73.200918
mock_eur = 0.937251
mock_cny = 6.826292
mock_source_json = f"""{{
    "success": true,
    "base": "USD",
    "date": "{datetime.date.today().isoformat()}",
    "rates": {{
        "USD": 1,
        "RUB": {mock_rub},
        "EUR": {mock_eur},
        "CNY": {mock_cny}
    }}
}}"""


def test_convert(tmp_path: Path, requests_mock):
    currates._mock_database(str(tmp_path / 'currates.db'))
    requests_mock.get(mock_source.url, text=mock_source_json)
    currates.update_rates([mock_source])

    res = currates.convert("€", "$", 9.85, lang_code="")
    assert f"{res:.2f}" == "10.51"

    res = currates.convert("EUR", "RUB", 9.85, lang_code="")
    assert f"{res:.2f}" == "769.30"

    res = currates.convert("¥", "RUB", 9.85, lang_code="zh")
    assert f"{res:.2f}" == "105.63"
