from src.data_agent.analysis import cagr


def caption_for_line(df, plan, group_by=None):
    x_col, y_col = plan["x"], plan["y"]
    first_year, last_year = df[x_col].min(), df[x_col].max()

    if group_by and group_by in df.columns:
        parts = []

        for key, group in df.groupby(group_by):
            group = group.sort_values(x_col)

            start_val = group[group[x_col] == first_year][y_col].mean()
            end_val = group[group[x_col] == last_year][y_col].mean()

            rate = cagr(
                start_val,
                end_val,
                last_year - first_year
            )

            if rate is not None:
                parts.append(
                    f"{key} grew at a CAGR of {rate:.1f}%"
                )

        return (
            f"{y_col} by {x_col} "
            f"({first_year}-{last_year}). "
            + "; ".join(parts)
            + "."
        )

    grouped = df.groupby(x_col)[y_col].mean()

    rate = cagr(
        grouped.iloc[0],
        grouped.iloc[-1],
        last_year - first_year
    )

    rate_text = (
        f"a CAGR of {rate:.1f}%"
        if rate is not None
        else "an undefined growth rate"
    )

    return (
        f"{y_col} rose from {grouped.iloc[0]:.1f} "
        f"in {first_year} to {grouped.iloc[-1]:.1f} "
        f"in {last_year} ({rate_text})."
    )


def caption_for_bar(df, plan):
    x_col, y_col = plan["x"], plan["y"]

    grouped = (
        df.groupby(x_col)[y_col]
        .mean()
        .sort_values(ascending=False)
    )

    top = grouped.index[0]

    return (
        f"Average {y_col} by {x_col}. "
        f"Highest: {top} ({grouped.iloc[0]:.1f})."
    )