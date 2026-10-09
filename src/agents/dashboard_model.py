from typing import Optional

from pydantic import BaseModel

from src.agents.models import UnifiedAnalysis


class KeyMetric(BaseModel):
    label: str
    value: str
    context: Optional[str] = None   # e.g. "2015-2023" or "vs. Karnataka"


class ChartRef(BaseModel):
    path: str
    caption: str
    chart_type: str
    reason: str


class ClaimRef(BaseModel):
    statement: str
    source_ids: list[str]


class SourceRef(BaseModel):
    id: str
    title: str
    url: str
    year: Optional[int] = None


class DashboardData(BaseModel):
    question: str
    summary: str
    key_metrics: list[KeyMetric] = []
    insights: list[str] = []
    charts: list[ChartRef] = []
    research_claims: list[ClaimRef] = []
    conflicts: list[str] = []
    sources: list[SourceRef] = []
    limitations: list[str] = []
    warnings: list[str] = []
    has_research: bool = False
    has_data: bool = False


def _build_summary(unified):
    parts = []
    if unified.research.answered and unified.research.overview:
        parts.append(unified.research.overview)
    if unified.data.used and unified.data.profile:
        parts.append(
            f"Dataset analyzed: {unified.data.profile.get('rows', '?')} rows "
            f"from {unified.data.dataset_path}."
        )
    if not parts:
        parts.append("No research or data findings were available for this question.")
    return " ".join(parts)


def _build_key_metrics(unified, max_metrics=4):
    metrics = []
    if unified.data.used and unified.data.stats:
        for col, stats in list(unified.data.stats.items())[:max_metrics]:
            if stats.get("mean") is not None:
                metrics.append(KeyMetric(
                    label=f"Average {col}", value=f"{stats['mean']:.2f}",
                    context=f"range {stats.get('min')}\u2013{stats.get('max')}",
                ))
    return metrics[:max_metrics]


def build_dashboard_data(unified: UnifiedAnalysis) -> DashboardData:
    """The single conversion point from analysis output to display-ready data.
    Nothing here calls an LLM or touches Pandas directly -- it only reshapes
    what UnifiedAnalysis already computed."""
    return DashboardData(
        question=unified.question,
        summary=_build_summary(unified),
        key_metrics=_build_key_metrics(unified),
        insights=unified.insights,
        charts=[ChartRef(**c) for c in unified.data.charts],
        research_claims=[
            ClaimRef(statement=c["statement"], source_ids=c["source_ids"])
            for c in unified.research.claims
        ],
        conflicts=unified.research.conflicts,
        sources=[SourceRef(**s.model_dump()) for s in unified.sources],
        limitations=unified.limitations,
        warnings=unified.warnings,
        has_research=unified.research.answered,
        has_data=unified.data.used,
    )