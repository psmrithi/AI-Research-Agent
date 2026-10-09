import re


def split_into_chunks(text, chunk_size=800, overlap=150):
    """Split text into overlapping chunks of roughly chunk_size characters.

    Splits on sentence boundaries where possible, so chunks don't cut words
    or ideas in half. Overlap keeps context from being lost at chunk edges.
    """
    text = re.sub(r"\s+", " ", text or "").strip()
    if not text:
        return []
    if len(text) <= chunk_size:
        return [text]

    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks, current = [], ""

    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= chunk_size:
            current = f"{current} {sentence}".strip()
        else:
            if current:
                chunks.append(current)

            tail = current[-overlap:] if overlap and current else ""
            current = f"{tail} {sentence}".strip()

    if current:
        chunks.append(current)

    return chunks


def chunk_source(source, chunk_size=800, overlap=150):
    """Split one Source's .text into chunks, each carrying its parent's metadata."""
    pieces = split_into_chunks(source.text, chunk_size, overlap)
    chunks = []

    for i, piece in enumerate(pieces):
        chunks.append({
            "chunk_id": f"{source.id}-chunk{i}",
            "source_id": source.id,
            "title": source.title,
            "url": source.url,
            "year": source.year,
            "source_type": source.source_type,
            "text": piece,
        })

    return chunks