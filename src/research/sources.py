from typing import Literal

from pydantic import BaseModel


class Source(BaseModel):
    id: str
    title: str
    url: str
    year: int | None = None
    authors: list[str] = []
    source_type: Literal["paper", "web", "report", "dataset"] = "web"
    text: str


def format_sources_for_prompt(sources):
    """Turn a list of Source objects into numbered text blocks for the LLM."""
    blocks = []

    for s in sources:
        year = f" ({s.year})" if s.year else ""
        blocks.append(f"[{s.id}] {s.title}{year}\n{s.text}")

    return "\n\n".join(blocks)