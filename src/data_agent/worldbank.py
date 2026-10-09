import pandas as pd

from src.utils.http import request_with_retry

BASE_URL = "https://api.worldbank.org/v2"

COLUMNS = [
    "country_code",
    "country",
    "indicator_id",
    "indicator",
    "year",
    "value"
]


def parse_worldbank_items(items):
    """Turn the API's list of observations into a list of flat dictionaries."""
    rows = []

    for item in items or []:
        rows.append({
            "country_code": item["country"]["id"],
            "country": item["country"]["value"],
            "indicator_id": item["indicator"]["id"],
            "indicator": item["indicator"]["value"],
            "year": int(item["date"]),
            "value": item["value"],
        })

    return rows


def rows_to_dataframe(rows):
    df = pd.DataFrame(rows, columns=COLUMNS)

    df["value"] = pd.to_numeric(
        df["value"],
        errors="coerce"
    )

    return df


def fetch_indicator(
    indicator_id,
    countries=("IN",),
    start=2015,
    end=2023
):
    """Download one indicator for one or more countries."""

    url = (
        f"{BASE_URL}/country/"
        f"{';'.join(countries)}"
        f"/indicator/{indicator_id}"
    )

    rows = []
    page = 1

    while True:
        params = {
            "format": "json",
            "date": f"{start}:{end}",
            "per_page": 1000,
            "page": page,
        }

        payload = request_with_retry(
            "GET",
            url,
            params=params
        ).json()

        if (
            not isinstance(payload, list)
            or len(payload) < 2
            or payload[1] is None
        ):
            raise ValueError(
                f"World Bank returned no data for {indicator_id}: {payload}"
            )

        meta, items = payload[0], payload[1]

        rows.extend(
            parse_worldbank_items(items)
        )

        if page >= int(meta.get("pages", 1)):
            break

        page += 1

    return rows_to_dataframe(rows)


def fetch_many(
    indicator_ids,
    countries=("IN",),
    start=2015,
    end=2023
):
    frames = [
        fetch_indicator(
            indicator,
            countries,
            start,
            end
        )
        for indicator in indicator_ids
    ]

    return pd.concat(
        frames,
        ignore_index=True
    )


def to_wide(long_df):
    """Convert long format into wide format."""

    wide = long_df.pivot(
        index=["country", "year"],
        columns="indicator_id",
        values="value"
    )

    wide.columns.name = None

    return wide.reset_index()
    