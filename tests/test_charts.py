from pathlib import Path

import pandas as pd

from src.data_agent.charts import draw_chart, save_chart, suggest_chart


def test_suggests_line_for_year_column():
    df = pd.DataFrame({"year": [2020, 2021], "value": [1, 2]})
    plan = suggest_chart(df, value_col="value", year_col="year")
    assert plan["chart_type"] == "line"


def test_suggests_bar_for_few_categories():
    df = pd.DataFrame({"state": ["A", "B", "C"], "value": [1, 2, 3]})
    plan = suggest_chart(df, value_col="value", category_col="state")
    assert plan["chart_type"] == "bar"


def test_suggests_histogram_for_many_categories():
    df = pd.DataFrame({
        "id": [f"item_{i}" for i in range(30)],
        "value": range(30)
    })
    plan = suggest_chart(df, value_col="value", category_col="id")
    assert plan["chart_type"] == "histogram"


def test_suggests_scatter_for_two_numeric_columns_no_year_or_category():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    plan = suggest_chart(df, value_col="a")
    assert plan["chart_type"] == "scatter"


def test_falls_back_to_histogram():
    df = pd.DataFrame({"a": [1, 2, 3]})
    plan = suggest_chart(df, value_col="a")
    assert plan["chart_type"] == "histogram"


def test_draw_and_save_creates_png_and_metadata(tmp_path):
    df = pd.DataFrame({
        "year": [2020, 2021, 2022],
        "value": [10, 20, 15]
    })

    plan = suggest_chart(
        df,
        value_col="value",
        year_col="year"
    )

    fig = draw_chart(
        df,
        plan,
        title="Test"
    )

    path = save_chart(
        fig,
        tmp_path / "chart.png",
        plan,
        "A test caption"
    )

    assert Path(path).exists()
    assert (tmp_path / "chart.meta.json").exists()