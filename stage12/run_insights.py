import json
import sys

from google.genai import errors

from src.agents.graph import build_graph


question = " ".join(sys.argv[1:]) or (
    "How has electric vehicle adoption changed, "
    "and what factors are driving it?"
)

app = build_graph()

try:
    final_state = app.invoke({"question": question})
except errors.APIError as error:
    raise SystemExit(f"Gemini error: {error.message}")


print("INSIGHTS:")

for insight in final_state["unified_analysis"]["insights"]:
    print(f"  - {insight}")


print("\nWARNINGS:")

for w in final_state["unified_analysis"]["warnings"]:
    print(f"  - {w}")