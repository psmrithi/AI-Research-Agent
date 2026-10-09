import json
import sys

from google.genai import errors

from src.agents.graph import build_graph


question = " ".join(sys.argv[1:]) or (
    "How has electric vehicle adoption changed, and what factors are driving it?"
)

app = build_graph()

try:
    final_state = app.invoke({"question": question})
except errors.APIError as error:
    raise SystemExit(f"Gemini error: {error.message}")


print("=" * 70)
print("UNIFIED ANALYSIS (structured):\n")
print(
    json.dumps(
        final_state["unified_analysis"],
        indent=2,
        default=str,
    )
)

print("\n" + "=" * 70)
print("Chart file:", final_state.get("chart_path"))
print("Chart caption:", final_state.get("chart_caption"))