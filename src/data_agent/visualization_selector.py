import re

from src.data_agent.analysis import correlation_matrix
from src.data_agent.captions import caption_for_bar, caption_for_line
from src.data_agent.charts import (
    correlation_heatmap,
    draw_chart,
    save_chart,
    suggest_chart,
)


OUTPUT_DIR = "outputs/charts"

TREND_WORDS = (
    "trend",
    "over time",
    "growth",
    "change",
    "adoption",
    "increase",
    "decrease",
)

COMPARE_WORDS = (
    "compare",
    "comparison",
    "across",
    "between",
    "highest",
    "lowest",
    "which",
)

RELATE_WORDS = (
    "relationship",
    "correlation",
    "correlate",
    "versus",
    " vs ",
    "related to",
)


def _slugify(text):
    return re.sub(
        r"[^a-z0-9]+",
        "_",
        text.lower(),
    ).strip("_")


def _wants(question, keywords):
    q = (question or "").lower()
    return any(k in q for k in keywords)


def select_visualizations(
    df,
    question,
    label,
    max_charts=2,
):
    """Decide which 1-2 charts are genuinely useful for this question and dataset,
    instead of blindly generating every possible chart type.
    """
    year_col = "year" if "year" in df.columns else None

    group_by = next(
        (
            c
            for c in ("state", "country")
            if c in df.columns
        ),
        None,
    )

    numeric_cols = df.select_dtypes("number").columns.tolist()

    value_candidates = [
        c
        for c in numeric_cols
        if c != year_col
    ]

    if not value_candidates:
        return []

    value_col = value_candidates[0]

    can_trend = year_col is not None

    can_compare = (
        group_by is not None
        and df[group_by].nunique() <= 15
    )

    can_relate = len(value_candidates) >= 2

    wants_trend = _wants(
        question,
        TREND_WORDS,
    )

    wants_compare = _wants(
        question,
        COMPARE_WORDS,
    )

    wants_relate = _wants(
        question,
        RELATE_WORDS,
    )

    candidates = []

    if can_trend:
        candidates.append(
            (
                0
                if (
                    wants_trend
                    or not (
                        wants_compare
                        or wants_relate
                    )
                )
                else 1,
                "trend",
            )
        )

    if can_compare:
        candidates.append(
            (
                0 if wants_compare else 2,
                "compare",
            )
        )

    if can_relate:
        candidates.append(
            (
                0 if wants_relate else 3,
                "relate",
            )
        )

    if not candidates:
        candidates.append(
            (0, "distribution")
        )

    candidates.sort(
        key=lambda c: c[0]
    )

    chosen_kinds = []

    for _, kind in candidates:
        if kind not in chosen_kinds:
            chosen_kinds.append(kind)

        if len(chosen_kinds) >= max_charts:
            break

    results = []

    for kind in chosen_kinds:
        result = _build_chart(
            kind,
            df,
            value_col,
            year_col,
            group_by,
            label,
        )

        if result:
            results.append(result)

    return results


def _build_chart(
    kind,
    df,
    value_col,
    year_col,
    group_by,
    label,
):
    if kind == "trend":
        plan = suggest_chart(
            df,
            value_col=value_col,
            year_col=year_col,
        )

        fig = draw_chart(
            df,
            plan,
            title=f"{value_col} over time",
            group_by=group_by,
        )

        caption = caption_for_line(
            df,
            plan,
            group_by=group_by,
        )

        reason = (
            "A time column and either the question or "
            "the data suggested a trend was relevant."
        )

    elif kind == "compare":
        plan = suggest_chart(
            df,
            value_col=value_col,
            category_col=group_by,
        )

        fig = draw_chart(
            df,
            plan,
            title=f"{value_col} by {group_by}",
        )

        caption = caption_for_bar(
            df,
            plan,
        )

        reason = (
            f"The question or data suggested "
            f"comparing '{group_by}' groups."
        )

    elif kind == "relate":
        corr = correlation_matrix(df)

        fig = correlation_heatmap(
            corr,
            title="Correlation between numeric columns",
        )

        caption = (
            "Correlation between the numeric columns "
            "in this dataset."
        )

        plan = {
            "chart_type": "heatmap"
        }

        reason = (
            "Multiple numeric columns and the question "
            "suggested checking their relationship."
        )

    else:
        plan = suggest_chart(
            df,
            value_col=value_col,
        )

        fig = draw_chart(
            df,
            plan,
            title=f"Distribution of {value_col}",
        )

        caption = (
            f"Distribution of {value_col}."
        )

        reason = (
            "No time or category column was available, "
            "so a distribution was shown instead."
        )

    path = (
        f"{OUTPUT_DIR}/"
        f"auto_{_slugify(label)}_{kind}.png"
    )

    save_chart(
        fig,
        path,
        plan,
        caption,
    )

    return {
        "path": path,
        "caption": caption,
        "chart_type": plan["chart_type"],
        "reason": reason,
    }