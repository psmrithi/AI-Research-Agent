from unittest.mock import MagicMock

import src.agents.insight_node as insight_node_module
from src.agents.insight_node import InsightList, insight_node


def test_skips_llm_when_no_stats_or_research():
    result = insight_node({"question": "Q", "warnings": []})
    assert result["insights"] == []


def test_keeps_only_grounded_insights(monkeypatch):
    fake_result = InsightList(
        insights=[
            "Average price was 12.5 lakh.",
            "Sales hit 999999 units.",
        ]
    )

    monkeypatch.setattr(
        insight_node_module,
        "ask_json",
        MagicMock(return_value=fake_result),
    )

    state = {
        "question": "Q",
        "data_stats": {
            "price": {
                "mean": 12.5,
                "min": 9.0,
                "max": 16.0,
            }
        },
        "research_summary": None,
        "warnings": [],
    }

    result = insight_node(state)

    assert result["insights"] == [
        "Average price was 12.5 lakh."
    ]
    assert any(
        "discarded" in w
        for w in result["warnings"]
    )