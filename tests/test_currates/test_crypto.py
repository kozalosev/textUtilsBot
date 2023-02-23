import datetime
from strconv import currates
from strconv.currates.extractors import iso_date
from pathlib import Path

from . import test_fiat

mock_source = currates.DataSource('mock_source', 'http://localhost/crypto',
                                  status_checker=lambda json: json['status']['error_code'] == 0,
                                  rates_extractor=lambda json: {x['symbol']: (1 / x['quote']['USD']['price'])
                                                                for x in json['data']},
                                  date_extractor=iso_date('status.timestamp'))
mock_eth = 1644.6620025731618
mock_source_json = f"""{{
    "status": {{
        "timestamp": "{datetime.datetime.utcnow().date().isoformat()}T05:07:57.566Z",
        "error_code": 0
    }},
    "data": [
        {{
            "symbol": "ETH",
            "quote": {{
                "USD": {{
                    "price": {mock_eth}
                }}
            }}
        }}
    ]
}}"""


def test_convert(tmp_path: Path, requests_mock):
    currates._mock_database(str(tmp_path / 'currates.db'))
    requests_mock.get(test_fiat.mock_source.url, text=test_fiat.mock_source_json)
    requests_mock.get(mock_source.url, text=mock_source_json)
    currates.update_rates([test_fiat.mock_source, mock_source])

    res = currates.convert("ETH", "RUB", 1, lang_code="")
    assert f"{res:.2f}" == "120390.77"
