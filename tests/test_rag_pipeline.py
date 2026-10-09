from unittest.mock import MagicMock

from src.rag import pipeline as pipeline_module
from src.research.summarizer import Claim, ResearchSummary


class FakeStore:
    def __init__(self, chunks):
        self.chunks = chunks

    def search(self, query, top_k):
        return self.chunks


def test_returns_not_answered_when_no_chunks(monkeypatch):
    monkeypatch.setattr(
        pipeline_module,
        "retrieve",
        lambda *a, **k: []
    )

    result = pipeline_module.answer_with_rag(
        FakeStore([]),
        "irrelevant question"
    )

    assert result["answered"] is False
    assert result["sources"] == []


def test_returns_summary_when_chunks_found(monkeypatch):
    fake_chunk = {
        "chunk_id": "c1",
        "source_id": "S1",
        "distance": 0.1,
        "text": "text",
        "title": "T",
        "url": "https://x.org",
        "year": 2022,
        "source_type": "paper",
    }

    monkeypatch.setattr(
        pipeline_module,
        "retrieve",
        lambda *a, **k: [fake_chunk]
    )

    fake_summary = ResearchSummary(
        overview="overview",
        claims=[
            Claim(
                statement="a claim",
                source_ids=["S1"]
            )
        ],
        conflicts=[],
        gaps=[],
    )

    monkeypatch.setattr(
        pipeline_module,
        "summarize",
        MagicMock(return_value=fake_summary)
    )

    result = pipeline_module.answer_with_rag(
        FakeStore([fake_chunk]),
        "a question"
    )

    assert result["answered"] is True
    assert result["summary"].overview == "overview"
    assert result["citation_problems"] == []