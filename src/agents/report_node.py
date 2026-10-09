def report_node(state):
    lines = [
        f"# Research Question\n\n{state['question']}\n"
    ]

    if state.get("research_answered"):
        summary = state["research_summary"]

        lines.append(
            f"## Research Findings\n\n{summary.overview}\n"
        )

        lines.append("### Claims\n")

        for claim in summary.claims:
            lines.append(
                f"- {claim.statement} "
                f"[{', '.join(claim.source_ids)}]"
            )

        if summary.conflicts:
            lines.append("\n### Conflicting Findings\n")
            lines.extend(
                f"- {conflict}"
                for conflict in summary.conflicts
            )

        if summary.gaps:
            lines.append("\n### Gaps\n")
            lines.extend(
                f"- {gap}"
                for gap in summary.gaps
            )

        lines.append("\n### Research Sources\n")

        for source in state["research_sources"]:
            lines.append(
                f"- [{source.id}] {source.title} "
                f"({source.year or 'n/a'}) - {source.url}"
            )

    elif state.get("needs_research"):
        lines.append(
            f"## Research Findings\n\n"
            f"Not available: {state.get('research_reason')}\n"
        )

    if state.get("data_used"):
        lines.append(
            f"\n## Data Analysis\n\n"
            f"Dataset: `{state['dataset_path']}`\n"
        )

        lines.append(
            f"Rows: {state['data_profile']['rows']}, "
            f"Columns: {state['data_profile']['columns']}\n"
        )

        lines.append("### Key Statistics\n")

        for col, stats in state["data_stats"].items():
            lines.append(
                f"- **{col}**: "
                f"mean={stats['mean']}, "
                f"min={stats['min']}, "
                f"max={stats['max']}"
            )

    elif state.get("needs_data"):
        lines.append(
            "\n## Data Analysis\n\n"
            "No matching dataset was found in the catalog.\n"
        )

    if state.get("warnings"):
        lines.append("\n## Limitations\n")

        lines.extend(
            f"- {warning}"
            for warning in state["warnings"]
        )

    return {
        "final_report": "\n".join(lines)
    }