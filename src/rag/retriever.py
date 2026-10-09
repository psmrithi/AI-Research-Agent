DEFAULT_DISTANCE_THRESHOLD = 1.0


def retrieve(
    store,
    query,
    top_k=8,
    distance_threshold=DEFAULT_DISTANCE_THRESHOLD,
    max_per_source=3,
):
    """Retrieve relevant chunks for a query, filtered by relevance and source diversity."""

    candidates = store.search(query, top_k=top_k * 3)

    relevant = [
        c for c in candidates
        if c["distance"] <= distance_threshold
    ]

    kept = []
    per_source_count = {}

    for chunk in relevant:
        source_id = chunk["source_id"]

        if per_source_count.get(source_id, 0) >= max_per_source:
            continue

        kept.append(chunk)
        per_source_count[source_id] = (
            per_source_count.get(source_id, 0) + 1
        )

        if len(kept) >= top_k:
            break

    return kept


def chunks_to_sources(chunks):
    """Rebuild Source-like objects from retrieved chunks."""

    from src.research.sources import Source

    grouped = {}

    for c in chunks:
        grouped.setdefault(c["source_id"], []).append(c["text"])

    sources = []

    for source_id, texts in grouped.items():
        sample = next(
            c for c in chunks
            if c["source_id"] == source_id
        )

        sources.append(Source(
    id=source_id,
    title=sample["title"],
    url=sample["url"],
    year=sample["year"] or None,
    source_type=(
        sample["source_type"]
        if sample["source_type"] in {"paper", "web", "report", "dataset"}
        else "web"
    ),
    text=" [...] ".join(texts),
))
    return sources