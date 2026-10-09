from google.genai import errors

from src.research.sources import Source
from src.research.summarizer import check_citations, summarize


SOURCES = [
    Source(
        id="S1",
        title="Sunville Bike-Share Reaches Milestone",
        year=2023,
        url="https://example.com/sunville-news",
        source_type="web",
        text=(
            "Sunville launched its bike-share program in 2019 with 200 bikes. "
            "By 2023 the fleet had grown to 1,500 bikes, and annual rides "
            "reached 2.1 million."
        ),
    ),
    Source(
        id="S2",
        title="Sunville Transport Survey Report",
        year=2024,
        url="https://example.com/sunville-report",
        source_type="report",
        text=(
            "The city survey attributes the growth mainly to protected bike "
            "lanes built in 2021 and lower fares. It records 2.4 million rides "
            "in 2023."
        ),
    ),
    Source(
        id="S3",
        title="Weather and Urban Cycling in Sunville",
        year=2022,
        url="https://example.com/sunville-paper",
        source_type="paper",
        authors=["A. Example"],
        text=(
            "The study finds that rainfall reduces bike-share rides by about "
            "30% on rainy days. It does not examine fares or infrastructure."
        ),
    ),
]


def show(question):
    print("=" * 70)
    print("QUESTION:", question)

    summary = summarize(question, SOURCES)

    print("\nOVERVIEW:", summary.overview)

    print("\nCLAIMS:")
    for claim in summary.claims:
        print(f"  - {claim.statement}  [{', '.join(claim.source_ids)}]")

    print("\nCONFLICTS:", summary.conflicts or "none")
    print("GAPS:", summary.gaps or "none")

    problems = check_citations(summary, SOURCES)

    print(
        "\nCITATION CHECK:",
        "OK" if not problems else problems
    )


if __name__ == "__main__":
    try:
        show("How did Sunville's bike-share program grow, and why?")
        show("What was the average age of Sunville bike-share riders?")

    except errors.APIError as error:
        print(f"Gemini API error {error.code}: {error.message}")

    except (RuntimeError, ValueError) as error:
        print(f"Problem: {error}")
  
    Source(
    id="S4",
    title="Sunville Bike-Share Statistics",
    url="https://example.com/s4",
    year=2024,
    source_type="report",
    text="The Sunville bike-share fleet had 1,200 bikes in 2023.",
),