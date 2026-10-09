from src.research.search import search_all
from src.research.summarizer import summarize, check_citations


def main():
    question = "How is machine learning being used in official statistics?"

    print(f"QUESTION: {question}\n")

    # Step 1: Search research papers
    sources = search_all(question, max_results=3)

    print(f"\nSOURCES FOUND: {len(sources)}")

    for source in sources:
        print(f"{source.id}: {source.title}")

    if not sources:
        print("No sources found.")
        return

    # Step 2: Give the sources to the grounded summarizer
    summary = summarize(question, sources)

    print("\nOVERVIEW:")
    print(summary.overview)

    print("\nCLAIMS:")
    for claim in summary.claims:
        print(f"- {claim.statement} [{', '.join(claim.source_ids)}]")

    print("\nCONFLICTS:")
    for conflict in summary.conflicts:
        print(f"- {conflict}")

    print("\nGAPS:")
    for gap in summary.gaps:
        print(f"- {gap}")

    # Step 3: Check citations
    problems = check_citations(summary, sources)

    print("\nCITATION CHECK:")

    if problems:
        for problem in problems:
            print(f"- {problem}")
    else:
        print("OK")


if __name__ == "__main__":
    main()