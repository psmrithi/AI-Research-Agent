import json
from pathlib import Path

import pandas as pd


def load_table(path):
    path = Path(path)

    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)

    if path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(path)

    raise ValueError(f"Unsupported file type: {path.suffix}")


def profile_dataframe(df):
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "columns_list": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": {
            col: int(value)
            for col, value in df.isna().sum().items()
        },
        "duplicate_rows": int(df.duplicated().sum()),
    }


def save_dataset(df, path, source=None, description=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(path, index=False)

    metadata = {
        "source": source,
        "description": description,
        "rows": int(df.shape[0]),
        "columns": list(df.columns),
    }

    metadata_path = path.with_suffix(".metadata.json")

    with open(metadata_path, "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2)

    print(f"Saved dataset: {path}")
    print(f"Saved metadata: {metadata_path}")