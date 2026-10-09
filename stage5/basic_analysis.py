from src.data_agent.loaders import load_table


df = load_table("data/raw/worldbank_sample_long.csv")

# Remove rows with missing values
df = df.dropna(subset=["value"])


print("=== Average value by country ===")
print(df.groupby("country")["value"].mean())


print("\n=== Average value by indicator ===")
print(df.groupby("indicator_id")["value"].mean())


print("\n=== Number of records by country ===")
print(df.groupby("country").size())


print("\n=== India data ===")
print(df[df["country"] == "India"].head(10))