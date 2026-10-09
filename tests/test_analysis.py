import pandas as pd

from src.data_agent.analysis import (
    describe_numeric,
    find_outliers_iqr,
    yearly_growth,
    cagr,
    correlation_matrix,
)


def test_describe_numeric():
    df = pd.DataFrame({
        "value": [10, 20, 30]
    })

    result = describe_numeric(df)

    assert result["value"]["count"] == 3
    assert result["value"]["mean"] == 20.0
    assert result["value"]["median"] == 20.0
    assert result["value"]["min"] == 10.0
    assert result["value"]["max"] == 30.0


def test_find_outliers_iqr():
    df = pd.DataFrame({
        "value": [10, 11, 12, 13, 100]
    })

    result = find_outliers_iqr(
        df,
        "value",
    )

    assert result["value"].tolist() == [100]


def test_find_outliers_iqr_grouped():
    df = pd.DataFrame({
        "state": [
            "A", "A", "A", "A", "A",
            "B", "B", "B", "B", "B",
        ],
        "value": [
            10, 11, 12, 13, 100,
            20, 21, 22, 23, 24,
        ],
    })

    result = find_outliers_iqr(
        df,
        "value",
        group_by="state",
    )

    assert len(result) == 1
    assert result.iloc[0]["value"] == 100


def test_yearly_growth():
    df = pd.DataFrame({
        "year": [2020, 2021, 2022],
        "value": [100, 120, 180],
    })

    result = yearly_growth(
        df,
        "value",
    )

    assert pd.isna(result.iloc[0]["growth_percent"])
    assert round(
        result.iloc[1]["growth_percent"],
        2,
    ) == 20.0
    assert round(
        result.iloc[2]["growth_percent"],
        2,
    ) == 50.0


def test_yearly_growth_grouped():
    df = pd.DataFrame({
        "state": ["A", "A", "B", "B"],
        "year": [2020, 2021, 2020, 2021],
        "value": [100, 150, 200, 220],
    })

    result = yearly_growth(
        df,
        "value",
        group_by=["state"],
    )

    a_growth = result[
        result["state"] == "A"
    ].iloc[1]["growth_percent"]

    b_growth = result[
        result["state"] == "B"
    ].iloc[1]["growth_percent"]

    assert a_growth == 50.0
    assert round(b_growth, 2) == 10.0

def test_cagr():
    result = cagr(
        100,
        121,
        2,
    )

    assert round(result, 2) == 10.0


def test_correlation_matrix():
    df = pd.DataFrame({
        "x": [1, 2, 3],
        "y": [2, 4, 6],
    })

    result = correlation_matrix(df)

    assert result["x"]["y"] == 1.0
    assert result["y"]["x"] == 1.0