import pandas as pd


class CleaningLog:
    """Records every change made to a DataFrame, in order."""

    def __init__(self):
        self.steps = []

    def add(self, action, detail):
        self.steps.append({"action": action, "detail": detail})

    def as_list(self):
        return list(self.steps)


def standardize_text_column(df, column, log):
    """Trim whitespace and fix inconsistent capitalization."""
    before = df[column].nunique()
    df[column] = df[column].astype(str).str.strip().str.title()
    after = df[column].nunique()

    if before != after:
        log.add(
            "standardize_text",
            f"'{column}': {before} unique values -> {after}"
        )

    return df


def numbers_from_text(df, column, log):
    """Convert a text column like '1,200' into a real numeric column."""

    original_missing = df[column].isna().sum()

    cleaned = (
        df[column]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    numeric = pd.to_numeric(cleaned, errors="coerce")

    n_failed = numeric.isna().sum() - original_missing

    df[column] = numeric

    log.add(
        "numbers_from_text",
        f"'{column}' converted to numeric; "
        f"{n_failed} values could not be parsed"
    )

    return df


def drop_duplicate_rows(df, log):
    n_before = len(df)

    df = df.drop_duplicates().reset_index(drop=True)

    removed = n_before - len(df)

    if removed:
        log.add(
            "drop_duplicates",
            f"Removed {removed} duplicate row(s)"
        )

    return df


def handle_missing(df, column, strategy, log):
    """strategy: 'drop_rows' or 'median'."""

    n_missing = df[column].isna().sum()

    if n_missing == 0:
        return df

    if strategy == "drop_rows":
        df = df.dropna(subset=[column]).reset_index(drop=True)

        log.add(
            "handle_missing",
            f"'{column}': dropped {n_missing} row(s) with missing values"
        )

    elif strategy == "median":
        fill_value = df[column].median()

        df[column] = df[column].fillna(fill_value)

        log.add(
            "handle_missing",
            f"'{column}': filled {n_missing} missing value(s) "
            f"with median ({fill_value:.2f})"
        )

    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    return df


def handle_missing_grouped(df, column, group_by, log):
    """Fill missing values using the median within each group."""

    n_missing = df[column].isna().sum()

    if n_missing == 0:
        return df

    df[column] = df.groupby(group_by)[column].transform(
        lambda s: s.fillna(s.median())
    )

    remaining = df[column].isna().sum()

    log.add(
        "handle_missing_grouped",
        f"'{column}' grouped by '{group_by}': "
        f"filled {n_missing - remaining} value(s) with group median; "
        f"{remaining} still missing (empty group)"
    )

    return df


def clean_ev_practice_data(df):
    """The full cleaning pipeline for the synthetic EV practice dataset."""

    log = CleaningLog()

    df = df.copy()

    df = standardize_text_column(df, "state", log)
    df = numbers_from_text(df, "ev_registrations", log)
    df = drop_duplicate_rows(df, log)
    df = handle_missing_grouped(
        df,
        "avg_price_lakh",
        "state",
        log
    )

    return df, log