import json

from src.data_agent.analysis import (
    correlation_matrix,
    describe_numeric,
    find_outliers_iqr,
)

from src.data_agent.loaders import (
    load_table,
    profile_dataframe,
)


df = load_table(
    "data/processed/worldbank_analysis.csv"
)


print(
    "PROFILE:",
    json.dumps(
        profile_dataframe(df),
        indent=2
    )
)


print("\nSTATS BY INDICATOR:")

for indicator_id, group in df.groupby("indicator_id"):

    print(f"\n-- {indicator_id} --")

    print(
        json.dumps(
            describe_numeric(
                group[
                    ["value", "growth_percent"]
                ]
            ),
            indent=2
        )
    )


print(
    "\nOUTLIER GROWTH YEARS "
    "(per country+indicator):"
)


outliers = find_outliers_iqr(
    df.dropna(
        subset=["growth_percent"]
    ),
    "growth_percent",
    group_by=[
        "country",
        "indicator_id"
    ],
)


print(
    outliers[
        [
            "country",
            "indicator_id",
            "year",
            "growth_percent",
        ]
    ]
)