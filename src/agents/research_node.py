from google.genai import errors

from src.rag.chunking import chunk_source
from src.rag.pipeline import answer_with_rag
from src.rag.vector_store import VectorStore
from src.research.search import search_all

_store = None


def get_store():
    global _store

    if _store is None:
        _store = VectorStore()

    return _store


def research_node(state):
    store = get_store()
    query = state.get("search_query") or state["question"]

    try:
        fresh_sources = search_all(
            query,
            max_results=3
        )

        search_warnings = []

        chunks = [
            chunk
            for source in fresh_sources
            for chunk in chunk_source(source)
        ]

        store.add_chunks(chunks)

    except Exception as error:
        search_warnings = [
            f"Source gathering failed: {error}"
        ]

    try:
        result = answer_with_rag(
            store,
            state["question"],
            search_query=query
        )

    except errors.APIError as error:
        return {
            "research_answered": False,
            "research_reason": f"Gemini error: {error.message}",
            "research_summary": None,
            "research_sources": [],
            "warnings": (
                state.get("warnings", [])
                + search_warnings
            ),
        }

    return {
        "research_answered": result["answered"],
        "research_reason": result["reason"],
        "research_summary": result["summary"],
        "research_sources": result["sources"],
        "warnings": (
            state.get("warnings", [])
            + search_warnings
        ),
    }