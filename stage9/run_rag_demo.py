from google.genai import errors

from src.rag.pipeline import answer_with_rag
from src.rag.vector_store import VectorStore

store = VectorStore()
print(f"Vector store has {store.count()} chunks.\n")

questions = [
    ("What factors support solar energy growth?", "solar energy India policy growth"),
    ("What is the capital of a fictional planet called Zorgon?", None),
]

for question, search_query in questions:
    print("=" * 70)
    print("QUESTION:", question)
    try:
        result = answer_with_rag(store, question, search_query=search_query)
    except errors.APIError as error:
        print(f"Gemini API error {error.code}: {error.message}")
        continue

    if not result["answered"]:
        print("NOT ANSWERED:", result["reason"])
        continue

    print(f"\nUsed {len(result['chunks_used'])} chunks from {len(result['sources'])} source(s).")
    print("\nOVERVIEW:", result["summary"].overview)
    print("\nCLAIMS:")
    for claim in result["summary"].claims:
        print(f"  - {claim.statement}  [{', '.join(claim.source_ids)}]")
    print("\nCONFLICTS:", result["summary"].conflicts or "none")
    print("GAPS:", result["summary"].gaps or "none")
    print("CITATION CHECK:", result["citation_problems"] or "OK")