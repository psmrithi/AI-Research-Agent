_model = None


def get_embedding_model():
    """Load the sentence-transformer model once (lazy), so importing this file is cheap."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def embed_texts(texts):
    """Turn a list of strings into a list of embedding vectors (lists of floats)."""
    if not texts:
        return []
    model = get_embedding_model()
    vectors = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return vectors.tolist()