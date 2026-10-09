import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # no GUI needed; just save files
import matplotlib.pyplot as plt
import pandas as pd


def suggest_chart(df, value_col, year_col=None, category_col=None):
    """Pick a chart type based on the shape of the data. Returns a plan dict, not a picture."""
    numeric_cols = df.select_dtypes("number").columns.tolist()

    if year_col and year_col in df.columns:
        return {"chart_type": "line", "x": year_col, "y": value_col,
                "reason": f"'{year_col}' looks like a time column, so a trend line fits best."}

    if category_col and category_col in df.columns:
        n_categories = df[category_col].nunique()
        if n_categories <= 15:
            return {"chart_type": "bar", "x": category_col, "y": value_col,
                     "reason": f"'{category_col}' has {n_categories} categories, so a bar chart compares them clearly."}
        return {"chart_type": "histogram", "x": value_col,
                 "reason": f"'{category_col}' has too many ({n_categories}) categories for readable bars; "
                            f"showing the distribution of '{value_col}' instead."}

    if len(numeric_cols) >= 2:
        return {"chart_type": "scatter", "x": numeric_cols[0], "y": numeric_cols[1],
                 "reason": f"Two numeric columns present, so a scatter plot can reveal a relationship."}

    return {"chart_type": "histogram", "x": value_col,
             "reason": "No clear time or category column, so a distribution histogram is the safest default."}


def _new_figure():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    return fig, ax


def draw_chart(df, plan, title=None, group_by=None):
    """Render the chosen chart_type. Returns the Matplotlib Figure (not yet saved)."""
    fig, ax = _new_figure()
    chart_type = plan["chart_type"]

    if chart_type == "line":
        if group_by and group_by in df.columns:
            for key, group in df.groupby(group_by):
                ax.plot(group[plan["x"]], group[plan["y"]], marker="o", label=str(key))
            ax.legend(fontsize=8)
        else:
            grouped = df.groupby(plan["x"])[plan["y"]].mean()
            ax.plot(grouped.index, grouped.values, marker="o")
        ax.set_xlabel(plan["x"])
        ax.set_ylabel(plan["y"])

    elif chart_type == "bar":
        grouped = df.groupby(plan["x"])[plan["y"]].mean().sort_values(ascending=False)
        ax.bar(grouped.index.astype(str), grouped.values)
        ax.set_xlabel(plan["x"])
        ax.set_ylabel(f"Average {plan['y']}")
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    elif chart_type == "scatter":
        ax.scatter(df[plan["x"]], df[plan["y"]], alpha=0.6)
        ax.set_xlabel(plan["x"])
        ax.set_ylabel(plan["y"])

    elif chart_type == "histogram":
        ax.hist(df[plan["x"]].dropna(), bins=15)
        ax.set_xlabel(plan["x"])
        ax.set_ylabel("Count")

    else:
        raise ValueError(f"Unknown chart_type: {chart_type}")

    ax.set_title(title or f"{plan['chart_type'].title()} chart")
    fig.tight_layout()
    return fig


def correlation_heatmap(corr_dict, title="Correlation matrix"):
    """corr_dict comes from analysis.correlation_matrix()."""
    corr_df = pd.DataFrame(corr_dict)
    fig, ax = _new_figure()
    im = ax.imshow(corr_df.values, vmin=-1, vmax=1, cmap="RdBu_r")
    ax.set_xticks(range(len(corr_df.columns)))
    ax.set_xticklabels(corr_df.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(corr_df.index)))
    ax.set_yticklabels(corr_df.index)
    for i in range(len(corr_df.index)):
        for j in range(len(corr_df.columns)):
            ax.text(j, i, f"{corr_df.values[i, j]:.2f}", ha="center", va="center", fontsize=8)
    fig.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title(title)
    fig.tight_layout()
    return fig


def save_chart(fig, path, plan, caption):
    """Save a chart as PNG plus a .meta.json with its plan and caption, then close it."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=120)
    plt.close(fig)
    meta = {"file": path.name, "plan": plan, "caption": caption}
    path.with_suffix(".meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return path