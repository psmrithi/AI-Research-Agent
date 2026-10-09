from src.rag.vector_store import VectorStore

store = VectorStore()
print(f"Store has {store.count()} chunks.\n")

relevant_query = "solar energy India policy"
irrelevant_query = "recipe for chocolate chip cookies"

for label, query in [
    ("RELEVANT", relevant_query),
    ("IRRELEVANT", irrelevant_query)
]:
    hits = store.search(query, top_k=5)

    print(f"--- {label}: {query!r} ---")

    for hit in hits:
        print(
            f"  distance={hit['distance']:.3f}  "
            f"{hit['title'][:50]}"
        )

    print()