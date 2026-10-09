import numpy as np
import pandas as pd


def describe_numeric(df):
    """Standard descriptive statistics for every numeric column."""
    numeric = df.select_dtypes("number")

    if numeric.empty:
        return {}

    return {
        col: {
            "count": int(numeric[col].count()),
            "mean": round(float(numeric[col].mean()), 3),
            "median": round(float(numeric[col].median()), 3),
            "std": round(float(numeric[col].std()), 3)
            if numeric[col].count() > 1
            else None,
            "min": round(float(numeric[col].min()), 3),
            "max": round(float(numeric[col].max()), 3),
        }
        for col in numeric.columns
    }


def find_outliers_iqr(df, column, group_by=None):
    """Return rows whose value is an outlier by the IQR rule."""

    def flag(series):
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        low = q1 - 1.5 * iqr
        high = q3 + 1.5 * iqr

        return (series < low) | (series > high)

    if group_by:
        mask = df.groupby(group_by)[column].transform(flag)
    else:
        mask = flag(df[column])

    return df[mask.fillna(False)]


def yearly_growth(df, value_col, year_col="year", group_by=None):
    """Year-over-year percentage change."""

    df = df.sort_values(
        ([*group_by] if group_by else []) + [year_col]
    ).copy()

    if group_by:
        df["growth_percent"] = (
            df.groupby(group_by)[value_col].pct_change() * 100
        )
    else:
        df["growth_percent"] = (
            df[value_col].pct_change() * 100
        )

    return df


def cagr(start_value, end_value, periods):
    """Compound Annual Growth Rate as a percentage."""

    if start_value <= 0 or periods <= 0:
        return None

    return (
        ((end_value / start_value) ** (1 / periods)) - 1
    ) * 100


def correlation_matrix(df):
    numeric = df.select_dtypes("number")

    if numeric.shape[1] < 2:
        return {}

    return numeric.corr(numeric_only=True).round(3).to_dict()