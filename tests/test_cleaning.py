import pandas as pd

from src.data_agent.cleaning import (
    CleaningLog,
    standardize_text_column,
    numbers_from_text,
    drop_duplicate_rows,
    handle_missing,
    handle_missing_grouped,
)


def test_standardize_text_column():
    df = pd.DataFrame({
        "state": [" tamil nadu ", "KARNATAKA", "Tamil Nadu"]
    })

    log = CleaningLog()

    result = standardize_text_column(
        df,
        "state",
        log,
    )

    assert result["state"].tolist() == [
        "Tamil Nadu",
        "Karnataka",
        "Tamil Nadu",
    ]


def test_numbers_from_text():
    df = pd.DataFrame({
        "value": ["1,200", "3,500", "800"]
    })

    log = CleaningLog()

    result = numbers_from_text(
        df,
        "value",
        log,
    )

    assert result["value"].tolist() == [
        1200,
        3500,
        800,
    ]

    assert pd.api.types.is_numeric_dtype(
        result["value"]
    )


def test_drop_duplicate_rows():
    df = pd.DataFrame({
        "year": [2020, 2020, 2021],
        "value": [100, 100, 200],
    })

    log = CleaningLog()

    result = drop_duplicate_rows(
        df,
        log,
    )

    assert len(result) == 2
    assert result["value"].tolist() == [
        100,
        200,
    ]


def test_handle_missing_median():
    df = pd.DataFrame({
        "value": [10, 20, None, 30]
    })

    log = CleaningLog()

    result = handle_missing(
        df,
        "value",
        "median",
        log,
    )

    assert result["value"].isna().sum() == 0
    assert result["value"].tolist() == [
        10,
        20,
        20,
        30,
    ]