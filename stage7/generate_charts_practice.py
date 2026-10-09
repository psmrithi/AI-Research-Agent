from src.data_agent.captions import caption_for_bar, caption_for_line
from src.data_agent.charts import draw_chart, save_chart, suggest_chart
from src.data_agent.cleaning import clean_ev_practice_data
from src.data_agent.loaders import load_table


raw = load_table("data/sample/practice_ev_registrations_SYNTHETIC.csv")
clean, _ = clean_ev_practice_data(raw)


plan1 = suggest_chart(
    clean,
    value_col="ev_registrations",
    year_col="year"
)

print("Plan 1:", plan1)

fig1 = draw_chart(
    clean,
    plan1,
    title="EV Registrations Over Time (by State)",
    group_by="state"
)

caption1 = caption_for_line(
    clean,
    plan1,
    group_by="state"
)

save_chart(
    fig1,
    "outputs/charts/ev_registrations_trend.png",
    plan1,
    caption1
)

print("Caption 1:", caption1)


plan2 = suggest_chart(
    clean,
    value_col="avg_price_lakh",
    category_col="state"
)

print("\nPlan 2:", plan2)

fig2 = draw_chart(
    clean,
    plan2,
    title="Average EV Price by State"
)

caption2 = caption_for_bar(
    clean,
    plan2
)

save_chart(
    fig2,
    "outputs/charts/avg_price_by_state.png",
    plan2,
    caption2
)

print("Caption 2:", caption2)

print("\nSaved charts to outputs/charts/. Open them to check they look right.")