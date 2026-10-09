import xml.etree.ElementTree as ET
from urllib.parse import quote

from src.research.sources import Source
from src.utils.http import request_with_retry


ARXIV_API_URL = "https://export.arxiv.org/api/query"


def search_arxiv(query, max_results=5):
    """Search arXiv and return results as Source objects."""

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
    }

    response = request_with_retry(
        "GET",
        ARXIV_API_URL,
        params=params,
    )

    response.raise_for_status()

    root = ET.fromstring(response.text)

    namespace = {
        "atom": "http://www.w3.org/2005/Atom",
    }

    sources = []

    for entry in root.findall("atom:entry", namespace):
        title = entry.findtext(
            "atom:title",
            default="",
            namespaces=namespace,
        ).strip()

        summary = entry.findtext(
            "atom:summary",
            default="",
            namespaces=namespace,
        ).strip()

        published = entry.findtext(
            "atom:published",
            default="",
            namespaces=namespace,
        )

        year = int(published[:4]) if published else None

        url = ""
        for link in entry.findall("atom:link", namespace):
            if link.attrib.get("type") == "text/html":
                url = link.attrib.get("href", "")
                break

        authors = []

        for author in entry.findall("atom:author", namespace):
            name = author.findtext(
                "atom:name",
                default="",
                namespaces=namespace,
            )

            if name:
                authors.append(name.strip())

        sources.append(
            Source(
                id="",
                title=" ".join(title.split()),
                url=url,
                year=year,
                authors=authors,
                source_type="paper",
                text=" ".join(summary.split()),
            )
        )

    return sources