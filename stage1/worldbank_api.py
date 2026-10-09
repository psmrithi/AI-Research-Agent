import json
from pathlib import Path

import requests

BASE_URL = "https://api.worldbank.org/v2"


def fetch_indicator(country="IN", indicator="EG.FEC.RNEW.ZS", start=2015, end=2022):
    """Download one World Bank indicator as raw JSON."""
    url = f"{BASE_URL}/country/{country}/indicator/{indicator}"
    params = {"format": "json", "date": f"{start}:{end}", "per_page": 100}
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()   # raises an error for 404, 500, etc.
    return response.json()


def parse_indicator(payload):
    """Turn World Bank's raw JSON into a simple sorted list of {year, value}."""
    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        raise ValueError("Unexpected response format or no data returned")

    rows = []
    for item in payload[1]:
        rows.append({"year": int(item["date"]), "value": item["value"]})
    rows.sort(key=lambda row: row["year"])
    return rows


def save_json(data, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    try:
        payload = fetch_indicator()
        save_json(payload, Path(__file__).parent / "output" / "worldbank_raw.json")
        rows = parse_indicator(payload)
    except requests.exceptions.Timeout:
        print("The request timed out. Check your internet and try again.")
    except requests.exceptions.RequestException as error:
        print(f"Network/API error: {error}")
    except ValueError as error:
        print(f"Data problem: {error}")
    else:
        print("Renewable energy consumption (% of total), India")
        for row in rows:
            value = "missing" if row["value"] is None else f"{row['value']:.2f}"
            print(f"  {row['year']}: {value}")