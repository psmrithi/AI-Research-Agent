from src.rag.chunking import chunk_source, split_into_chunks


class FakeSource:
    def __init__(self, id, title, url, year, source_type, text):
        self.id = id
        self.title = title
        self.url = url
        self.year = year
        self.source_type = source_type
        self.text = text


def test_short_text_is_one_chunk():
    assert split_into_chunks("Short text.", chunk_size=800) == ["Short text."]


def test_long_text_splits_into_multiple_chunks():
    sentence = "This is one sentence about solar energy growth. "
    text = sentence * 40
    chunks = split_into_chunks(text, chunk_size=500, overlap=50)

    assert len(chunks) > 1
    assert all(len(c) <= 600 for c in chunks)


def test_empty_text_returns_no_chunks():
    assert split_into_chunks("") == []
    assert split_into_chunks(None) == []


def test_chunk_source_carries_metadata():
    source = FakeSource(
        "S1",
        "A Paper",
        "https://x.org",
        2022,
        "paper",
        "A short abstract.",
    )

    chunks = chunk_source(source)

    assert len(chunks) == 1
    assert chunks[0]["chunk_id"] == "S1-chunk0"
    assert chunks[0]["source_id"] == "S1"
    assert chunks[0]["year"] == 2022