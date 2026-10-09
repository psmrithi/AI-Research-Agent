from src.rag.retriever import chunks_to_sources, retrieve
from src.research.summarizer import check_citations, summarize


def answer_with_rag(store, question, search_query=None, top_k=8, distance_threshold=1.0):
    """The full RAG loop. Returns a dict with the summary, sources used, and diagnostics."""
    query = search_query or question
    chunks = retrieve(store, query, top_k=top_k, distance_threshold=distance_threshold)

    if not chunks:
        return {
            "answered": False,
            "reason": "No sufficiently relevant information found in the vector store "
                      "for this question.",
            "summary": None,
            "sources": [],
            "chunks_used": [],
        }

    sources = chunks_to_sources(chunks)
    summary = summarize(question, sources)
    problems = check_citations(summary, sources)

    return {
        "answered": True,
        "reason": None,
        "summary": summary,
        "sources": sources,
        "chunks_used": chunks,
        "citation_problems": problems,
    }