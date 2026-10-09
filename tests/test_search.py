from src.research.search import _dedupe_sources
from src.research.sources import Source


def make_source(title, url):
    return Source(
        id="",
        title=title,
        url=url,
        year=2024,
        authors=["Test Author"],
        source_type="paper",
        text="Test abstract",
    )


def test_dedupe_by_url():
    sources = [
        make_source("Paper One", "https://example.com/paper"),
        make_source("Same Paper", "https://example.com/paper"),
    ]

    result = _dedupe_sources(sources)

    assert len(result) == 1


def test_dedupe_by_title_when_url_missing():
    sources = [
        make_source("Paper One", ""),
        make_source("paper one", ""),
    ]

    result = _dedupe_sources(sources)

    assert len(result) == 1


def test_different_sources_are_kept():
    sources = [
        make_source("Paper One", "https://example.com/one"),
        make_source("Paper Two", "https://example.com/two"),
    ]

    result = _dedupe_sources(sources)

    assert len(result) == 2


def test_empty_source_is_ignored():
    sources = [
        make_source("", ""),
    ]

    result = _dedupe_sources(sources)

    assert len(result) == 0