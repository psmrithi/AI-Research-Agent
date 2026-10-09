import re
from pathlib import Path

from src.data_agent.captions import caption_for_bar, caption_for_line
from src.data_agent.charts import draw_chart, save_chart, suggest_chart

OUTPUT_DIR = "outputs/charts"


def _slugify(text):
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def auto_chart_for_dataframe(df, label, title=None):
    """Pick a sensible chart, render it, and save it."""

    year_col = "year" if "year" in df.columns else None

    group_by = next(
        (c for c in ("state", "country") if c in df.columns),
        None
    )

    numeric_cols = df.select_dtypes("number").columns.tolist()

    value_candidates = [
        c for c in numeric_cols
        if c != year_col
    ]

    if not value_candidates:
        return None, None, None

    value_col = value_candidates[0]

    plan = suggest_chart(
        df,
        value_col=value_col,
        year_col=year_col,
        category_col=group_by if not year_col else None,
    )

    fig = draw_chart(
        df,
        plan,
        title=title or f"{value_col} ({label})",
        group_by=group_by if plan["chart_type"] == "line" else None,
    )

    if plan["chart_type"] == "line":
        caption = caption_for_line(
            df,
            plan,
            group_by=group_by
        )
    elif plan["chart_type"] == "bar":
        caption = caption_for_bar(df, plan)
    else:
        caption = f"{plan['chart_type'].title()} chart of {value_col}."

    path = Path(OUTPUT_DIR) / f"auto_{_slugify(label)}.png"

    save_chart(
        fig,
        path,
        plan,
        caption
    )

    return str(path), caption, plan