from typing import Annotated, Optional, TypedDict

from src.research.summarizer import ResearchSummary


class AgentState(TypedDict, total=False):
    """The single object that flows through every node in the graph."""

    question: str

    # --- set by the planner node ---
    needs_research: bool
    needs_data: bool
    search_query: str
    data_keywords: list

    # --- set by the research node ---
    research_summary: Optional[ResearchSummary]
    research_sources: list
    research_answered: bool
    research_reason: Optional[str]

    # --- set by the data node ---
    data_used: bool
    dataset_path: Optional[str]
    data_profile: Optional[dict]
    data_stats: Optional[dict]
    insights: list
    # --- set by the final/report node ---
    final_report: Optional[str]
    warnings: Annotated[list, lambda left, right: left + right]
        # --- new in Stage 11 ---
    charts: list
    unified_analysis: Optional[dict]