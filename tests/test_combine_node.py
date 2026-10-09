
from src.agents.combine_node import combine_node
from src.research.summarizer import Claim, ResearchSummary
from src.research.sources import Source


def base_state(**overrides):
    state = {
        "question": "Q",
        "needs_research": True,
        "needs_data": True,
        "research_answered": False,
        "research_summary": None,
        "research_sources": [],
        "research_reason": None,
        "data_used": False,
        "dataset_path": None,
        "data_profile": None,
        "data_stats": None,
        "chart_path": None,
        "chart_caption": None,
        "warnings": [],
    }

    state.update(overrides)
    return state


def test_combine_handles_full_state():
    summary = ResearchSummary(
        overview="overview text",
        claims=[
            Claim(
                statement="a claim",
                source_ids=["S1"],
            )
        ],
        conflicts=["conflict"],
        gaps=["gap"],
    )

    source = Source(
        id="S1",
        title="T",
        url="https://x.org",
        year=2022,
        text="text",
    )

    state = base_state(
        research_answered=True,
        research_summary=summary,
        research_sources=[source],
        data_used=True,
        dataset_path="d.csv",
        data_profile={"rows": 5},
        data_stats={"x": {}},
        chart_path="outputs/charts/x.png",
        chart_caption="cap",
    )

    unified = combine_node(state)["unified_analysis"]

    assert unified["question"] == "Q"
    assert unified["research"]["overview"] == "overview text"
    assert unified["data"]["dataset_path"] == "d.csv"
    assert unified["sources"][0]["id"] == "S1"
    assert unified["limitations"] == []


def test_combine_adds_limitations_when_unanswered():
    state = base_state(
        research_reason="no sources"
    )

    unified = combine_node(state)["unified_analysis"]

    assert any(
        "research" in limitation.lower()
        for limitation in unified["limitations"]
    )

    assert any(
        "dataset" in limitation.lower()
        for limitation in unified["limitations"]
    )


def test_combine_skips_limitations_when_not_needed():
    state = base_state(
        needs_research=False,
        needs_data=False,
    )

    unified = combine_node(state)["unified_analysis"]

    assert unified["limitations"] == []

