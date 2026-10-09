from src.research.arxiv_search import search_arxiv
from src.research.semantic_scholar import search_semantic_scholar
from src.research.sources import Source


def _dedupe_sources(sources):
    """Remove duplicate sources using title or URL."""
    seen = set()
    unique = []

    for source in sources:
        title_key = source.title.strip().lower()
        url_key = source.url.strip().lower()

        key = url_key or title_key

        if not key or key in seen:
            continue

        seen.add(key)
        unique.append(source)

    return unique


def search_all(query, max_results=5):
    """Search multiple research providers and return normalized sources."""

    all_sources = []

    providers = [
        ("arXiv", search_arxiv),
        ("Semantic Scholar", search_semantic_scholar),
    ]

    for provider_name, search_function in providers:
        try:
            results = search_function(query, max_results=max_results)
            all_sources.extend(results)
            print(f"[search] {provider_name}: {len(results)} results")

        except Exception as error:
            print(f"[search] {provider_name} failed: {error}")

    unique_sources = _dedupe_sources(all_sources)

    numbered_sources = []

    for index, source in enumerate(unique_sources, start=1):
        numbered_sources.append(
            Source(
                id=f"S{index}",
                title=source.title,
                url=source.url,
                year=source.year,
                authors=source.authors,
                source_type=source.source_type,
                text=source.text,
            )
        )

    return numbered_sources