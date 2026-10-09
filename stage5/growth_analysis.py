from src.data_agent.loaders import load_table


df = load_table("data/raw/worldbank_sample_long.csv")

df = df.dropna(subset=["value"])

# Sort before calculating yearly change
df = df.sort_values(["country", "indicator_id", "year"])

# Calculate percentage change within each country and indicator
df["growth_percent"] = (
    df.groupby(["country", "indicator_id"])["value"]
    .pct_change()
    * 100
)

print("=== Data with yearly growth ===")
print(
    df[
        [
            "country",
            "indicator_id",
            "year",
            "value",
            "growth_percent",
        ]
    ].head(20)
)
