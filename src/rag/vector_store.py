from pathlib import Path

import chromadb

from src.rag.embeddings import embed_texts

DEFAULT_PATH = "vector_store/chroma_db"


class VectorStore:
    def __init__(self, path=DEFAULT_PATH, collection_name="research_chunks"):
        Path(path).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=str(path))

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=None
        )

    def add_chunks(self, chunks):
        """Add chunks to the vector database."""
        if not chunks:
            return 0

        existing = set(
            self.collection.get(
                ids=[c["chunk_id"] for c in chunks]
            )["ids"]
        )

        new_chunks = [
            c for c in chunks
            if c["chunk_id"] not in existing
        ]

        if not new_chunks:
            return 0

        texts = [c["text"] for c in new_chunks]
        vectors = embed_texts(texts)

        self.collection.add(
            ids=[c["chunk_id"] for c in new_chunks],
            embeddings=vectors,
            documents=texts,
            metadatas=[
                {
                    "source_id": c["source_id"],
                    "title": c["title"],
                    "url": c["url"],
                    "year": c["year"] or 0,
                    "source_type": c["source_type"],
                }
                for c in new_chunks
            ],
        )

        return len(new_chunks)

    def search(self, query, top_k=5):
        """Return the chunks most similar to the query."""
        if self.collection.count() == 0:
            return []

        query_vector = embed_texts([query])[0]

        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )

        hits = []

        for i in range(len(results["ids"][0])):
            hits.append({
                "chunk_id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "distance": results["distances"][0][i],
                **results["metadatas"][0][i],
            })

        return hits

    def count(self):
        return self.collection.count()