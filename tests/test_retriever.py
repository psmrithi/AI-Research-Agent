from src.rag.retriever import chunks_to_sources, retrieve


class FakeStore:
    def __init__(self, chunks):
        self.chunks = chunks

    def search(self, query, top_k):
        return self.chunks[:top_k]


def make_chunk(
    chunk_id,
    source_id,
    distance,
    text="some text",
    title="T",
    url="https://x.org",
    year=2022
):
    return {
        "chunk_id": chunk_id,
        "source_id": source_id,
        "distance": distance,
        "text": text,
        "title": title,
        "url": url,
        "year": year,
        "source_type": "paper",
    }


def test_filters_out_chunks_above_threshold():
    chunks = [
        make_chunk("c1", "S1", 0.3),
        make_chunk("c2", "S2", 1.8),
    ]

    kept = retrieve(
        FakeStore(chunks),
        "q",
        top_k=8,
        distance_threshold=1.0
    )

    assert [c["chunk_id"] for c in kept] == ["c1"]


def test_caps_chunks_per_source():
    chunks = [
        make_chunk(f"c{i}", "S1", 0.1)
        for i in range(5)
    ]

    kept = retrieve(
        FakeStore(chunks),
        "q",
        top_k=8,
        distance_threshold=1.0,
        max_per_source=2
    )

    assert len(kept) == 2


def test_returns_empty_when_nothing_relevant():
    chunks = [
        make_chunk("c1", "S1", 5.0)
    ]

    assert retrieve(
        FakeStore(chunks),
        "q",
        distance_threshold=1.0
    ) == []


def test_chunks_to_sources_joins_same_source_chunks():
    chunks = [
        make_chunk(
            "c1",
            "S1",
            0.1,
            text="first part"
        ),
        make_chunk(
            "c2",
            "S1",
            0.2,
            text="second part"
        ),
        make_chunk(
            "c3",
            "S2",
            0.1,
            text="other source"
        ),
    ]

    sources = chunks_to_sources(chunks)

    assert len(sources) == 2

    s1 = next(
        s for s in sources
        if s.id == "S1"
    )

    assert "first part" in s1.text
    assert "second part" in s1.text