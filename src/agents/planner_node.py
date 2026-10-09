from pydantic import BaseModel, Field

from src.llm.client import ask_json


class RoutingPlan(BaseModel):
    needs_research: bool = Field(
        description="True if papers/web sources should be searched"
    )
    needs_data: bool = Field(
        description="True if a dataset should be analyzed"
    )
    search_query: str = Field(
        description="3-6 keyword search query for finding sources"
    )
    data_keywords: list[str] = Field(
        description="Keywords describing what dataset is needed"
    )


SYSTEM = (
    "You are the routing module of a research and analytics agent. "
    "Decide whether the question needs research sources, numeric data analysis, or both. "
    "A question about causes, opinions, or explanations usually needs research. "
    "A question about trends, growth, or numbers over time usually needs data. "
    "Many questions need both."
)


def planner_node(state):
    plan = ask_json(
        f"Question: {state['question']}",
        RoutingPlan,
        system=SYSTEM
    )

    return {
        "needs_research": plan.needs_research,
        "needs_data": plan.needs_data,
        "search_query": plan.search_query,
        "data_keywords": plan.data_keywords,
        "warnings": [],
    }