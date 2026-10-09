from pydantic import BaseModel, Field

from src.llm.client import ask_json
from src.research.sources import format_sources_for_prompt


class Claim(BaseModel):
    statement: str
    source_ids: list[str] = Field(
        description="IDs such as S1, S2 that support this claim"
    )


class ResearchSummary(BaseModel):
    overview: str
    claims: list[Claim]
    conflicts: list[str] = Field(
        description="Places where sources disagree, naming the source IDs"
    )
    gaps: list[str] = Field(
        description="Parts of the question the sources do not answer"
    )


SYSTEM = """You are a careful research summarizer.
Rules:
1. Use ONLY the numbered sources provided. Never use outside knowledge.
2. Every claim must list the source IDs that directly support it.
3. If sources disagree, describe the disagreement in 'conflicts'. Do not pick a side.
4. If the sources do not answer part of the question, list it in 'gaps'. Do not guess.
5. Copy numbers exactly as written in the sources."""


def summarize(question, sources):
    prompt = f"Question: {question}\n\nSources:\n{format_sources_for_prompt(sources)}"
    return ask_json(prompt, ResearchSummary, system=SYSTEM)


def check_citations(summary, sources):
    """Return a list of problems. An empty list means the citations look valid."""
    valid_ids = {s.id for s in sources}
    problems = []

    for claim in summary.claims:
        if not claim.source_ids:
            problems.append(f"No citation: {claim.statement!r}")

        for sid in claim.source_ids:
            if sid not in valid_ids:
                problems.append(
                    f"Unknown source {sid!r} in claim: {claim.statement!r}"
                )

    return problems