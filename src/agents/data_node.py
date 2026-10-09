from src.data_agent.auto_chart import auto_chart_for_dataframe
from src.data_agent.analysis import describe_numeric
from src.data_agent.loaders import load_table, profile_dataframe
from src.data_agent.visualization_selector import select_visualizations


DATASET_CATALOG = {
    "ev": "data/processed/ev_practice_clean.csv",
    "electric vehicle": "data/processed/ev_practice_clean.csv",
    "renewable": "data/processed/worldbank_analysis.csv",
    "solar": "data/processed/worldbank_analysis.csv",
    "population": "data/processed/worldbank_analysis.csv",
    "gdp": "data/processed/worldbank_analysis.csv",
}


def pick_dataset(keywords):
    for keyword in keywords:
        for catalog_key, path in DATASET_CATALOG.items():
            if catalog_key in keyword.lower():
                return path

    return None


def data_node(state):
    path = pick_dataset(state.get("data_keywords", []))

    if not path:
        return {
            "data_used": False,
            "dataset_path": None,
            "data_profile": None,
            "data_stats": None,
            "charts": [],
            "warnings": (
                state.get("warnings", [])
                + ["No matching dataset found in the catalog."]
            ),
        }

    try:
        df = load_table(path)

    except (FileNotFoundError, ValueError) as error:
        return {
            "data_used": False,
            "dataset_path": path,
            "data_profile": None,
            "data_stats": None,
            "charts": [],
            "warnings": (
                state.get("warnings", [])
                + [f"Could not load dataset: {error}"]
            ),
        }

    profile = profile_dataframe(df)
    stats = describe_numeric(df)

    try:
        charts = select_visualizations(
            df,
            question=state.get("question", ""),
            label=path,
        )

    except (ValueError, KeyError) as error:
        return {
            "data_used": True,
            "dataset_path": path,
            "data_profile": profile,
            "data_stats": stats,
            "charts": [],
            "warnings": (
                state.get("warnings", [])
                + [f"Chart generation failed: {error}"]
            ),
        }

    return {
        "data_used": True,
        "dataset_path": path,
        "data_profile": profile,
        "data_stats": stats,
        "charts": charts,
        "warnings": state.get("warnings", []),
    }