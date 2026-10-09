from src.agents.models import (
    DataFindings,
    ResearchFindings,
    SourceRef,
    UnifiedAnalysis,
)


def combine_node(state):
    summary = state.get("research_summary")

    research = ResearchFindings(
        answered=bool(state.get("research_answered")),
        overview=summary.overview if summary else None,
        claims=[c.model_dump() for c in summary.claims] if summary else [],
        conflicts=summary.conflicts if summary else [],
        gaps=summary.gaps if summary else [],
        reason=state.get("research_reason"),
    )

    sources = [
        SourceRef(
            id=s.id,
            title=s.title,
            url=s.url,
            year=s.year,
        )
        for s in state.get("research_sources", [])
    ]

    data = DataFindings(
        used=bool(state.get("data_used")),
        dataset_path=state.get("dataset_path"),
        profile=state.get("data_profile"),
        stats=state.get("data_stats"),
        charts=state.get("charts", []),
    )

    limitations = []

    if state.get("needs_research") and not state.get("research_answered"):
        limitations.append(
            "No sufficiently relevant research sources were found."
        )

    if state.get("needs_data") and not state.get("data_used"):
        limitations.append(
            "No matching dataset was found for this question."
        )

    unified = UnifiedAnalysis(
        question=state["question"],
        research=research,
        data=data,
        sources=sources,
        limitations=limitations,
        warnings=state.get("warnings", []),
        insights=state.get("insights", []),
    )

    return {"unified_analysis": unified.model_dump()}