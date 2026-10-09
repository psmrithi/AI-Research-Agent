from google.genai import errors

from src.rag.chunking import chunk_source
from src.rag.vector_store import VectorStore
from src.research.search import search_all

query_for_sources = "solar energy India policy growth"
print(f"Searching for sources on: {query_for_sources}")

try:
    sources = search_all(query_for_sources)
    warnings = []
except (errors.APIError, RuntimeError) as error:
    raise SystemExit(f"Search failed: {error}")

print(f"Found {len(sources)} sources.", *warnings, sep="\n")

if not sources:
    raise SystemExit("No sources found, nothing to index.")

all_chunks = []

for s in sources:
    chunks = chunk_source(s)
    print(
        f"  [{s.id}] {s.title[:60]}... -> {len(chunks)} chunk(s)"
    )
    all_chunks.extend(chunks)

print(f"\nTotal chunks to index: {len(all_chunks)}")

store = VectorStore()

added = store.add_chunks(all_chunks)

print(f"Added {added} new chunk(s). Store now has {store.count()} total.")

print("\n=== Semantic search test ===")

test_queries = [
    "government policy supporting renewable energy",
    "cost of solar panels",
    "unrelated topic like ancient Roman history",
]

for q in test_queries:
    print(f"\nQuery: {q!r}")

    hits = store.search(q, top_k=3)

    for hit in hits:
        print(
            f"  distance={hit['distance']:.3f} "
            f"[{hit['source_id']}] "
            f"{hit['title'][:50]}"
        )
        print(f"    {hit['text'][:150]}...")