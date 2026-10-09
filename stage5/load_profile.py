from src.data_agent.loaders import load_table, profile_dataframe


df = load_table("data/raw/worldbank_sample_long.csv")

print("=== Loaded Data ===")
print(df.head())

print("\n=== Shape ===")
print(df.shape)

print("\n=== Profile ===")
print(profile_dataframe(df))