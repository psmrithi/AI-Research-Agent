
from pathlib import Path

import pandas as pd

import src.data_agent.auto_chart as auto_chart_module
from src.data_agent.auto_chart import auto_chart_for_dataframe


def test_returns_none_when_no_numeric_columns():
    df = pd.DataFrame({"name": ["a", "b"]})

    path, caption, plan = auto_chart_for_dataframe(
        df,
        label="test",
    )

    assert path is None
    assert caption is None
    assert plan is None


def test_generates_line_chart_for_year_data(tmp_path, monkeypatch):
    monkeypatch.setattr(
        auto_chart_module,
        "OUTPUT_DIR",
        str(tmp_path),
    )

    df = pd.DataFrame(
        {
            "year": [2020, 2021, 2022],
            "value": [10, 20, 15],
        }
    )

    path, caption, plan = auto_chart_for_dataframe(
        df,
        label="demo",
    )

    assert plan["chart_type"] == "line"
    assert path is not None
    assert Path(path).exists()
    assert caption is not None

