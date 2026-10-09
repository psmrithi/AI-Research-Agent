from src.data_agent.analysis import correlation_matrix
from src.data_agent.captions import caption_for_line
from src.data_agent.charts import (
    correlation_heatmap,
    draw_chart,
    save_chart,
    suggest_chart,
)
from src.data_agent.loaders import load_table


df = load_table("data/processed/worldbank_analysis.csv")

india = df[
    (df["country"] == "India")
    & (df["indicator_id"] == "EG.ELC.RNEW.ZS")
]


plan = suggest_chart(
    india,
    value_col="value",
    year_col="year"
)

fig = draw_chart(
    india,
    plan,
    title="India: Renewable Electricity Output (%)"
)

caption = caption_for_line(
    india,
    plan
)

save_chart(
    fig,
    "outputs/charts/india_renewable_trend.png",
    plan,
    caption
)

print("Caption:", caption)


wide_like = df.pivot_table(
    index=["country", "year"],
    columns="indicator_id",
    values="value"
).reset_index()

corr = correlation_matrix(wide_like)

fig2 = correlation_heatmap(
    corr,
    title="Correlation Between World Bank Indicators"
)

save_chart(
    fig2,
    "outputs/charts/worldbank_correlation.png",
    {"chart_type": "heatmap"},
    "Correlation across indicators."
)

print("Saved correlation heatmap.")