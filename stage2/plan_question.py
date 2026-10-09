from typing import Literal

from pydantic import BaseModel, Field

from src.llm.client import ask_json

class ResearchPlan(BaseModel):
    topic: str
    question_type: Literal[
        "trend_analysis",
        "comparison",
        "causal_explanation",
        "definition",
        "other",
    ]
    needs_research: bool = Field(
        description="True if papers/web sources are needed"
    )
    needs_data: bool = Field(
        description="True if a dataset should be analysed"
    )
    sub_questions: list[str] = Field(
        description="3 to 5 smaller questions to answer"
    )
    data_keywords: list[str] = Field(
        description="Keywords to search datasets with"
    )
    year_start: int | None = None
    year_end: int | None = None


SYSTEM = (
    "You are the planning module of a research agent. "
    "You only create plans. You never answer the question itself."
)


def main():
    import sys

    question = (
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "What are the main causes of climate change?"
    )

    plan = ask_json(
        question,
        ResearchPlan,
        system=SYSTEM,
    )

    print(plan.model_dump_json(indent=2))


if __name__ == "__main__":
    main()