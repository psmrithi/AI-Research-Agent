import pytest

from worldbank_api import parse_indicator


def fake_payload():
    return [
        {"page": 1, "pages": 1, "per_page": 100, "total": 3},
        [
            {"date": "2021", "value": 21.5},
            {"date": "2019", "value": None},
            {"date": "2020", "value": 20.0},
        ],
    ]


def test_parse_sorts_by_year():
    rows = parse_indicator(fake_payload())
    assert [row["year"] for row in rows] == [2019, 2020, 2021]


def test_parse_keeps_missing_values_as_none():
    rows = parse_indicator(fake_payload())
    assert rows[0]["value"] is None


def test_bad_payload_raises_error():
    with pytest.raises(ValueError):
        parse_indicator([{"message": [{"id": "120"}]}])