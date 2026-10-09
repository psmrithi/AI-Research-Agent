from pathlib import Path

import pandas as pd

import src.data_agent.visualization_selector as viz_module
from src.data_agent.visualization_selector import select_visualizations


def make_df():
    return pd.DataFrame({
        "year": [2020, 2021, 2022, 2020, 2021, 2022],
        "state": ["A", "A", "A", "B", "B", "B"],
        "value1": [10, 15, 20, 100, 150, 200],
        "value2": [5, 6, 7, 50, 55, 60],
    })


def test_relationship_question_prioritizes_relate(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        viz_module,
        "OUTPUT_DIR",
        str(tmp_path),
    )

    charts = select_visualizations(
        make_df(),
        "What is the correlation here?",
        label="t",
    )

    assert charts[0]["chart_type"] == "heatmap"


def test_ambiguous_question_defaults_to_trend_then_compare(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        viz_module,
        "OUTPUT_DIR",
        str(tmp_path),
    )

    charts = select_visualizations(
        make_df(),
        "Tell me about this data",
        label="t",
    )

    kinds = [
        c["chart_type"]
        for c in charts
    ]

    assert kinds[0] == "line"
    assert "bar" in kinds


def test_compare_question_prioritizes_bar(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        viz_module,
        "OUTPUT_DIR",
        str(tmp_path),
    )

    charts = select_visualizations(
        make_df(),
        "Compare states",
        label="t",
    )

    assert charts[0]["chart_type"] == "bar"


def test_no_numeric_columns_returns_empty():
    df = pd.DataFrame({
        "name": ["a", "b"]
    })

    assert (
        select_visualizations(
            df,
            "any question",
            label="t",
        )
        == []
    )


def test_respects_max_charts_limit(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        viz_module,
        "OUTPUT_DIR",
        str(tmp_path),
    )

    charts = select_visualizations(
        make_df(),
        "compare and correlate over time",
        label="t",
        max_charts=1,
    )

    assert len(charts) == 1


def test_chart_files_are_created(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        viz_module,
        "OUTPUT_DIR",
        str(tmp_path),
    )

    charts = select_visualizations(
        make_df(),
        "trend over time",
        label="t",
    )

    for chart in charts:
        assert Path(chart["path"]).exists()