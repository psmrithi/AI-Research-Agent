import sys

from google.genai import errors

from src.agents.graph import build_graph


question = " ".join(sys.argv[1:]) or (
    "Compare EV registrations across states and show "
    "how they've changed over time"
)


app = build_graph()

try:
    final_state = app.invoke({"question": question})

except errors.APIError as error:
    raise SystemExit(
        f"Gemini error: {error.message}"
    )


charts = final_state["unified_analysis"]["data"]["charts"]

print(
    f"Generated {len(charts)} chart(s):\n"
)

for chart in charts:
    print(
        f"  type={chart['chart_type']}  "
        f"file={chart['path']}"
    )

    print(
        f"    caption: {chart['caption']}"
    )

    print(
        f"    reason:  {chart['reason']}\n"
    )