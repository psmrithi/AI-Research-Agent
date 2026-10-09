import json

from src.data_agent.analysis import (
    correlation_matrix,
    describe_numeric,
    find_outliers_iqr,
    yearly_growth,
)

from src.data_agent.cleaning import clean_ev_practice_data

from src.data_agent.loaders import (
    load_table,
    profile_dataframe,
    save_dataset,
)

pd_display = __import__("pandas")
pd_display.set_option("display.width", 120)


raw = load_table(
    "data/sample/practice_ev_registrations_SYNTHETIC.csv"
)

print(
    "BEFORE:",
    json.dumps(profile_dataframe(raw), indent=2)
)


clean, log = clean_ev_practice_data(raw)


print("\nCLEANING LOG:")

for step in log.as_list():
    print(
        f"  - [{step['action']}] {step['detail']}"
    )


print(
    "\nAFTER:",
    json.dumps(profile_dataframe(clean), indent=2)
)


save_dataset(
    clean,
    "data/processed/ev_practice_clean.csv",
    source="Synthetic practice data, cleaned",
    description=(
        "Cleaned version of "
        "practice_ev_registrations_SYNTHETIC.csv"
    ),
)


print("\n=== Descriptive statistics ===")

print(
    json.dumps(
        describe_numeric(clean),
        indent=2
    )
)


print("\n=== Outliers (ev_registrations, per state) ===")

outliers = find_outliers_iqr(
    clean,
    "ev_registrations",
    group_by="state",
)

print(
    outliers[
        ["year", "state", "ev_registrations"]
    ]
)


print("\n=== Yearly growth (per state) ===")

growth = yearly_growth(
    clean,
    "ev_registrations",
    group_by=["state"],
)

print(
    growth[
        [
            "year",
            "state",
            "ev_registrations",
            "growth_percent",
        ]
    ].head(12)
)


print("\n=== Correlation matrix ===")

print(
    json.dumps(
        correlation_matrix(clean),
        indent=2
    )
)