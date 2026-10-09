from src.data_agent.loaders import load_table


df = load_table("data/raw/worldbank_sample_long.csv")

print("=== Original missing values ===")
print(df["value"].isna().sum())


# Remove rows where value is missing
clean_df = df.dropna(subset=["value"])

print("\n=== After removing missing values ===")
print(clean_df["value"].isna().sum())

print("\n=== Original shape ===")
print(df.shape)

print("\n=== New shape ===")
print(clean_df.shape)