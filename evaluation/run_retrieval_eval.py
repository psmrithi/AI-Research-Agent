import json
from pathlib import Path

from google.genai import errors

from src.rag.pipeline import answer_with_rag
from src.rag.vector_store import VectorStore

questions = json.loads(
    Path("evaluation/eval_questions.json").read_text(encoding="utf-8")
)

store = VectorStore()

results, correct = [], 0

for q in questions:
    try:
        result = answer_with_rag(
            store,
            q["question"],
            search_query=q["search_query"]
        )
    except errors.APIError as error:
        results.append({
            "id": q["id"],
            "verdict": "ERROR",
            "detail": str(error)
        })
        continue

    answered = result["answered"]
    matches_expectation = answered == q["should_answer"]

    terms_found = []

    if answered and q["expect_terms"]:
        full_text = result["summary"].overview + " ".join(
            c.statement for c in result["summary"].claims
        )

        terms_found = [
            t for t in q["expect_terms"]
            if t.lower() in full_text.lower()
        ]

    citation_ok = (
        not result.get("citation_problems")
        if answered
        else True
    )

    verdict = (
        "PASS"
        if matches_expectation and citation_ok
        else "FAIL"
    )

    correct += verdict == "PASS"

    results.append({
        "id": q["id"],
        "verdict": verdict,
        "answered": answered,
        "expected_answered": q["should_answer"],
        "terms_found": terms_found,
        "expected_terms": q["expect_terms"],
        "citation_ok": citation_ok,
    })

print(json.dumps(results, indent=2))
print(f"\n{correct}/{len(questions)} passed")