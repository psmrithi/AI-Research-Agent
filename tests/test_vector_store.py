import pytest

from src.rag import vector_store as vs_module
from src.rag.vector_store import VectorStore


@pytest.fixture(autouse=True)
def fake_embeddings(monkeypatch):
    """Use fast fake embeddings so tests don't load the real model."""

    def fake_embed(texts):
        vectors = []

        for text in texts:
            vec = [0.0] * 16

            for word in text.lower().split():
                vec[hash(word) % 16] += 1.0

            vectors.append(vec)

        return vectors

    monkeypatch.setattr(vs_module, "embed_texts", fake_embed)


def make_chunks():
    return [
        {
            "chunk_id": "S1-chunk0",
            "source_id": "S1",
            "title": "Solar growth",
            "url": "https://a.org",
            "year": 2022,
            "source_type": "paper",
            "text": "solar energy capacity increased",
        },
        {
            "chunk_id": "S2-chunk0",
            "source_id": "S2",
            "title": "Wind power",
            "url": "https://b.org",
            "year": 2021,
            "source_type": "paper",
            "text": "wind power turbines installed",
        },
    ]


def test_add_and_count(tmp_path):
    store = VectorStore(path=tmp_path / "db")

    added = store.add_chunks(make_chunks())

    assert added == 2
    assert store.count() == 2


def test_adding_same_chunks_twice_does_not_duplicate(tmp_path):
    store = VectorStore(path=tmp_path / "db")

    store.add_chunks(make_chunks())
    added_again = store.add_chunks(make_chunks())

    assert added_again == 0
    assert store.count() == 2


def test_search_returns_metadata(tmp_path):
    store = VectorStore(path=tmp_path / "db")

    store.add_chunks(make_chunks())
    hits = store.search("solar energy capacity", top_k=1)

    assert len(hits) == 1
    assert hits[0]["source_id"] == "S1"
    assert "distance" in hits[0]


def test_search_on_empty_store_returns_empty(tmp_path):
    store = VectorStore(path=tmp_path / "db")

    assert store.search("anything") == []