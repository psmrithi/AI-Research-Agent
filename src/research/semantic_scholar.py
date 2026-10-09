from src.research.sources import Source
from src.utils.http import request_with_retry


SEMANTIC_SCHOLAR_API_URL = (
    "https://api.semanticscholar.org/graph/v1/paper/search"
)


def search_semantic_scholar(query, max_results=5):
    """Search Semantic Scholar and return results as Source objects."""

    params = {
        "query": query,
        "limit": max_results,
        "fields": "title,abstract,url,year,authors",
    }

    response = request_with_retry(
        "GET",
        SEMANTIC_SCHOLAR_API_URL,
        params=params,
    )

    response.raise_for_status()

    data = response.json()

    sources = []

    for paper in data.get("data", []):
        title = paper.get("title") or ""
        abstract = paper.get("abstract") or ""
        url = paper.get("url") or ""
        year = paper.get("year")

        authors = [
            author.get("name", "")
            for author in paper.get("authors", [])
            if author.get("name")
        ]

        sources.append(
            Source(
                id="",
                title=" ".join(title.split()),
                url=url,
                year=year,
                authors=authors,
                source_type="paper",
                text=" ".join(abstract.split()),
            )
        )

    return sources