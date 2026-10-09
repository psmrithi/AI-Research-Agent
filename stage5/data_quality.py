from src.data_agent.loaders import load_table


df = load_table("data/raw/worldbank_sample_long.csv")

print("=== Missing values ===")
print(df.isna().sum())

print("\n=== Duplicate rows ===")
print(df.duplicated().sum())

print("\n=== Rows with missing value ===")
print(df[df["value"].isna()])