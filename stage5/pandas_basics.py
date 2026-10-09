import pandas as pd

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 20)

# Toy data, made up just for practice.
df = pd.DataFrame({
    "year": [2019, 2020, 2021, 2022, 2023],
    "state": ["A", "A", "A", "B", "B"],
    "sales": [100, 120, 90, 200, 260],
})

print("=== The table ===")
print(df)

print("\n=== Shape (rows, columns) ===")
print(df.shape)

print("\n=== Column types ===")
print(df.dtypes)

print("\n=== One column (a Series) ===")
print(df["sales"])

print("\n=== Filter rows: sales > 100 ===")
print(df[df["sales"] > 100])

print("\n=== Sort ===")
print(df.sort_values("sales", ascending=False))

print("\n=== Summary statistics ===")
print(df["sales"].describe())

print("\n=== Group by state ===")
print(df.groupby("state")["sales"].sum())

print("\n=== Yearly % change: the WRONG way ===")
df["growth_wrong"] = df["sales"].pct_change() * 100
print(df)

print("\n=== Yearly % change: the RIGHT way (per state) ===")
df["growth_right"] = df.groupby("state")["sales"].pct_change() * 100
print(df)