from src.agents.dashboard_model import build_dashboard_data
from src.agents.models import DataFindings, ResearchFindings, SourceRef, UnifiedAnalysis


def test_summary_combines_research_and_data():
    unified = UnifiedAnalysis(
        question="Q",
        research=ResearchFindings(
            answered=True,
            overview="Solar grew a lot."
        ),
        data=DataFindings(
            used=True,
            profile={"rows": 40},
            dataset_path="d.csv"
        ),
    )

    dashboard = build_dashboard_data(unified)

    assert "Solar grew a lot." in dashboard.summary
    assert "40 rows" in dashboard.summary


def test_summary_handles_nothing_available():
    unified = UnifiedAnalysis(
        question="Q",
        research=ResearchFindings(answered=False),
        data=DataFindings(used=False),
    )

    dashboard = build_dashboard_data(unified)

    assert "No research or data" in dashboard.summary
    assert dashboard.has_research is False
    assert dashboard.has_data is False


def test_key_metrics_built_from_stats():
    unified = UnifiedAnalysis(
        question="Q",
        research=ResearchFindings(answered=False),
        data=DataFindings(
            used=True,
            stats={
                "price": {
                    "mean": 12.5,
                    "min": 9.0,
                    "max": 16.0
                }
            }
        ),
    )

    dashboard = build_dashboard_data(unified)

    assert len(dashboard.key_metrics) == 1
    assert dashboard.key_metrics[0].label == "Average price"
    assert dashboard.key_metrics[0].value == "12.50"


def test_sources_and_claims_pass_through():
    unified = UnifiedAnalysis(
        question="Q",
        research=ResearchFindings(
            answered=True,
            claims=[
                {
                    "statement": "X happened",
                    "source_ids": ["S1"]
                }
            ],
        ),
        data=DataFindings(used=False),
        sources=[
            SourceRef(
                id="S1",
                title="T",
                url="https://x.org",
                year=2022
            )
        ],
    )

    dashboard = build_dashboard_data(unified)

    assert dashboard.research_claims[0].statement == "X happened"
    assert dashboard.sources[0].id == "S1"