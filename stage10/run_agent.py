import sys

from google.genai import errors

from src.agents.graph import build_graph


question = " ".join(sys.argv[1:]) or (
    "How has electric vehicle adoption changed, "
    "and what factors are driving it?"
)

app = build_graph()

try:
    final_state = app.invoke({
        "question": question
    })

except errors.APIError as error:
    raise SystemExit(
        f"Gemini error: {error.message}"
    )

print("=" * 70)
print("ROUTING DECISION:")
print(
    f"  needs_research={final_state.get('needs_research')}  "
    f"needs_data={final_state.get('needs_data')}"
)
print(
    f"  search_query={final_state.get('search_query')!r}"
)
print(
    f"  data_keywords={final_state.get('data_keywords')}"
)

print("\n" + "=" * 70)
print("FINAL REPORT:\n")
print(final_state["final_report"])