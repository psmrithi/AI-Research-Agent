import json
import pandas as pd
import requests

from src.data_agent.loaders import profile_dataframe, save_dataset
from src.data_agent.worldbank import fetch_many, to_wide


pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)


INDICATORS = [
    "EG.ELC.RNEW.ZS",
    "NY.GDP.PCAP.CD",
    "SP.POP.TOTL",
]

COUNTRIES = ["IN", "CN", "US"]


try:
    long_df = fetch_many(
        INDICATORS,
        COUNTRIES,
        start=2010,
        end=2022,
    )
except (requests.exceptions.RequestException, ValueError) as error:
    raise SystemExit(f"Could not fetch data: {error}")


save_dataset(
    long_df,
    "data/raw/worldbank_sample_long.csv",
    source="World Bank Open Data API (api.worldbank.org)",
    description=f"Indicators {INDICATORS} for {COUNTRIES}, 2010-2022",
)


print("=== LONG format (first 8 rows) ===")
print(long_df.head(8))

print("\nShape:")
print(long_df.shape)


wide = to_wide(long_df)

print("\n=== WIDE format ===")
print(wide.head(10))


print("\n=== Profile ===")
print(json.dumps(profile_dataframe(wide), indent=2))


print("\n=== India only ===")
print(wide[wide["country"] == "India"])