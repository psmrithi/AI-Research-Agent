from src.research.sources import Source, format_sources_for_prompt
from src.research.summarizer import Claim, ResearchSummary, check_citations


def make_sources():
    return [
        Source(
            id="S1",
            title="A",
            url="https://x.org",
            year=2023,
            text="Text one.",
        ),
        Source(
            id="S2",
            title="B",
            url="https://y.org",
            text="Text two.",
        ),
    ]


def make_summary(claims):
    return ResearchSummary(
        overview="o",
        claims=claims,
        conflicts=[],
        gaps=[],
    )


def test_valid_citations_pass():
    summary = make_summary(
        [Claim(statement="a", source_ids=["S1", "S2"])]
    )
    assert check_citations(summary, make_sources()) == []


def test_unknown_source_is_flagged():
    summary = make_summary(
        [Claim(statement="a", source_ids=["S9"])]
    )
    problems = check_citations(summary, make_sources())

    assert len(problems) == 1
    assert "S9" in problems[0]


def test_missing_citation_is_flagged():
    summary = make_summary(
        [Claim(statement="a", source_ids=[])]
    )
    assert len(check_citations(summary, make_sources())) == 1


def test_prompt_contains_ids_and_text():
    text = format_sources_for_prompt(make_sources())

    assert "[S1]" in text
    assert "Text two." in text

def test_valid_and_invalid_citations():
    summary = make_summary(
        [Claim(statement="a", source_ids=["S1", "S9"])]
    )

    problems = check_citations(summary, make_sources())

    assert len(problems) == 1
    assert "S9" in problems[0]