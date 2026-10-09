from src.agents.graph import route_after_planner
from src.agents.report_node import report_node


def test_route_returns_both_branches():
    state = {
        "needs_research": True,
        "needs_data": True
    }

    assert set(route_after_planner(state)) == {
        "research",
        "data"
    }


def test_route_returns_report_when_neither_needed():
    state = {
        "needs_research": False,
        "needs_data": False
    }

    assert route_after_planner(state) == ["report"]


def test_route_returns_single_research_branch():
    state = {
        "needs_research": True,
        "needs_data": False
    }

    assert route_after_planner(state) == ["research"]


def test_report_node_handles_missing_research_and_data():
    state = {
        "question": "Q",
        "needs_research": False,
        "needs_data": False,
        "warnings": []
    }

    result = report_node(state)

    assert "# Research Question" in result["final_report"]
    assert "Q" in result["final_report"]


def test_report_node_includes_warnings():
    state = {
        "question": "Q",
        "needs_research": False,
        "needs_data": False,
        "warnings": ["Something failed"]
    }

    result = report_node(state)

    assert "Something failed" in result["final_report"]