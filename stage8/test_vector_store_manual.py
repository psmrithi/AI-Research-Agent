from src.rag.chunking import chunk_source
from src.rag.vector_store import VectorStore


class FakeSource:
    def __init__(self):
        self.id = "TEST1"
        self.title = "Solar Energy in India"
        self.url = "https://example.com/solar"
        self.year = 2025
        self.source_type = "article"
        self.text = (
            "Solar energy is an important renewable energy source in India. "
            "Government policies support the growth of renewable energy. "
            "Solar power capacity has increased over the years. "
            "The cost of solar technology has also changed as adoption increases."
        )


source = FakeSource()

chunks = chunk_source(source)

print(f"Created {len(chunks)} chunk(s).")

store = VectorStore()

added = store.add_chunks(chunks)

print(f"Added {added} chunk(s).")
print(f"Total chunks in store: {store.count()}")

print("\n=== Search ===")

hits = store.search("government support for solar energy", top_k=1)

for hit in hits:
    print(f"Distance: {hit['distance']:.3f}")
    print(f"Title: {hit['title']}")
    print(f"Text: {hit['text']}")