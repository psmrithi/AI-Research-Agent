from src.data_agent.loaders import load_table, save_dataset


df = load_table("data/raw/worldbank_sample_long.csv")

df = df.dropna(subset=["value"])

df = df.sort_values(["country", "indicator_id", "year"])

df["growth_percent"] = (
    df.groupby(["country", "indicator_id"])["value"]
    .pct_change()
    * 100
)

save_dataset(
    df,
    "data/processed/worldbank_analysis.csv",
    source="World Bank Open Data API",
    description="Cleaned World Bank data with yearly percentage growth",
)

print("\n=== Final dataset ===")
print(df.head(10))
print("\nShape:", df.shape)