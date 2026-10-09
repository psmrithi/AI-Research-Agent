from pathlib import Path
import re

import pandas as pd
from google.genai import errors
from pydantic import BaseModel, Field

from src.agents.insight_validation import (
    collect_allowed_numbers,
    validate_insight,
)
from src.llm.client import ask_json


class InsightList(BaseModel):
    insights: list[str] = Field(
        description="3-5 short, plain-language, evidence-based insight sentences"
    )


SYSTEM = (
    "You are an evidence-based data analyst. "
    "Turn the supplied question, calculated dataset facts, statistics, "
    "and research findings into short, useful insights. "
    "Follow the user's question closely. "
    "If the question asks for a trend, describe the trend. "
    "If it asks for comparisons, compare the groups explicitly. "
    "If it asks for highest or lowest values, identify them explicitly. "
    "If it asks for a time period, respect that period when the supplied facts support it. "
    "Use ONLY facts and numbers supplied below. "
    "Never invent a number, percentage, year, state, ranking, or causal explanation. "
    "Do not claim that the research sources prove something when the research findings "
    "say that the requested evidence was not found. "
    "Keep each insight to one clear sentence. "
    "Prefer specific findings over generic statements such as 'the dataset has a mean'. "
    "If there is not enough evidence for a requested point, say that it cannot be "
    "determined from the supplied data instead of guessing."
)


def _format_stats(data_stats):
    if not data_stats:
        return "No dataset statistics available."

    lines = []

    for col, stats in data_stats.items():
        lines.append(
            f"- {col}: "
            f"mean={stats.get('mean')}, "
            f"median={stats.get('median')}, "
            f"min={stats.get('min')}, "
            f"max={stats.get('max')}"
        )

    return "\n".join(lines)


def _format_claims(research_summary):
    if not research_summary:
        return "No research findings available."

    if isinstance(research_summary, dict):
        overview = research_summary.get("overview", "")
        claims = research_summary.get("claims", [])
    else:
        overview = getattr(research_summary, "overview", "")
        claims = getattr(research_summary, "claims", [])

    lines = [f"Overview: {overview or 'No overview available.'}"]

    for claim in claims:
        if isinstance(claim, dict):
            statement = claim.get("statement", "")
        else:
            statement = getattr(claim, "statement", "")

        if statement:
            lines.append(f"- {statement}")

    return "\n".join(lines)


def _format_facts(facts):
    if not facts:
        return "No question-specific dataset facts were calculated."

    lines = []

    for key, value in facts.items():
        lines.append(f"- {key}: {value}")

    return "\n".join(lines)


def _extract_question_years(question):
    years = [
        int(value)
        for value in re.findall(r"\b(19\d{2}|20\d{2})\b", question or "")
    ]

    if len(years) >= 2:
        return min(years), max(years)

    return None, None


def _question_keywords(question):
    text = (question or "").lower()

    return {
        "trend": any(
            word in text
            for word in (
                "trend",
                "growth",
                "increase",
                "decrease",
                "over time",
                "change",
                "changed",
            )
        ),
        "compare": any(
            word in text
            for word in (
                "compare",
                "comparison",
                "state",
                "states",
                "group",
                "groups",
            )
        ),
        "extremes": any(
            word in text
            for word in (
                "highest",
                "lowest",
                "maximum",
                "minimum",
                "peak",
                "largest",
                "smallest",
            )
        ),
    }


def _calculate_question_facts(question, dataset_path):
    """
    Calculate deterministic facts from the dataset that the existing
    aggregate data_stats do not contain.

    This keeps exact values such as highest year and state averages
    grounded in Pandas rather than asking the LLM to calculate them.
    """

    if not dataset_path:
        return {}, {}

    path = Path(dataset_path)

    if not path.is_absolute():
        project_root = Path(__file__).resolve().parents[2]
        path = project_root / path

    if not path.exists():
        return {}, {}

    try:
        df = pd.read_csv(path)
    except Exception:
        return {}, {}

    if df.empty:
        return {}, {}

    facts = {}
    extra_numbers = set()

    keywords = _question_keywords(question)

    year_col = next(
        (
            col
            for col in df.columns
            if str(col).lower() == "year"
        ),
        None,
    )

    value_col = next(
        (
            col
            for col in df.columns
            if str(col).lower()
            in (
                "ev_registrations",
                "registrations",
                "sales",
                "value",
            )
        ),
        None,
    )

    group_col = next(
        (
            col
            for col in df.columns
            if str(col).lower()
            in (
                "state",
                "region",
                "category",
                "group",
            )
        ),
        None,
    )

    if value_col is None:
        numeric_columns = df.select_dtypes(
            include="number"
        ).columns.tolist()

        if numeric_columns:
            value_col = numeric_columns[0]

    if value_col is None:
        return {}, {}

    df[value_col] = pd.to_numeric(
        df[value_col],
        errors="coerce",
    )

    df = df.dropna(
        subset=[value_col]
    )

    if df.empty:
        return {}, {}

    start_year, end_year = _extract_question_years(
        question
    )

    if (
        year_col is not None
        and start_year is not None
        and end_year is not None
    ):

        df[year_col] = pd.to_numeric(
            df[year_col],
            errors="coerce",
        )

        period_df = df[
            df[year_col].between(
                start_year,
                end_year,
            )
        ].copy()

        if not period_df.empty:

            df_for_question = period_df

            facts["question_period"] = (
                f"{start_year}-{end_year}"
            )

            extra_numbers.update(
                [start_year, end_year]
            )

        else:
            df_for_question = df

    else:
        df_for_question = df

    # --------------------------------------------------------
    # TREND FACTS
    # --------------------------------------------------------

    if (
        keywords["trend"]
        and year_col is not None
    ):

        yearly = (
            df_for_question
            .groupby(year_col)[value_col]
            .sum()
            .sort_index()
        )

        if not yearly.empty:

            first_year = int(yearly.index.min())
            last_year = int(yearly.index.max())

            first_value = float(
                yearly.loc[first_year]
            )

            last_value = float(
                yearly.loc[last_year]
            )

            facts["first_year"] = first_year
            facts["first_year_registrations"] = round(
                first_value,
                3,
            )

            facts["last_year"] = last_year
            facts["last_year_registrations"] = round(
                last_value,
                3,
            )

            if first_value != 0:

                change_pct = (
                    (last_value - first_value)
                    / abs(first_value)
                ) * 100

                facts["change_from_first_to_last_pct"] = round(
                    change_pct,
                    2,
                )

                extra_numbers.add(
                    round(change_pct, 2)
                )

            extra_numbers.update(
                [
                    first_year,
                    last_year,
                    round(first_value, 3),
                    round(last_value, 3),
                ]
            )

    # --------------------------------------------------------
    # HIGHEST / LOWEST YEAR
    # --------------------------------------------------------

    if (
        keywords["extremes"]
        and year_col is not None
    ):

        yearly = (
            df_for_question
            .groupby(year_col)[value_col]
            .sum()
            .sort_index()
        )

        if not yearly.empty:

            highest_year = int(
                yearly.idxmax()
            )

            lowest_year = int(
                yearly.idxmin()
            )

            highest_value = float(
                yearly.max()
            )

            lowest_value = float(
                yearly.min()
            )

            facts["highest_year"] = highest_year
            facts["highest_year_registrations"] = round(
                highest_value,
                3,
            )

            facts["lowest_year"] = lowest_year
            facts["lowest_year_registrations"] = round(
                lowest_value,
                3,
            )

            extra_numbers.update(
                [
                    highest_year,
                    lowest_year,
                    round(highest_value, 3),
                    round(lowest_value, 3),
                ]
            )

    # --------------------------------------------------------
    # STATE / GROUP COMPARISON
    # --------------------------------------------------------

    if (
        keywords["compare"]
        and group_col is not None
    ):

        grouped = (
            df_for_question
            .groupby(group_col)[value_col]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        if not grouped.empty:

            highest_group = str(
                grouped.index[0]
            )

            lowest_group = str(
                grouped.index[-1]
            )

            highest_group_value = float(
                grouped.iloc[0]
            )

            lowest_group_value = float(
                grouped.iloc[-1]
            )

            facts["highest_group"] = (
                highest_group
            )

            facts["highest_group_average"] = round(
                highest_group_value,
                3,
            )

            facts["lowest_group"] = (
                lowest_group
            )

            facts["lowest_group_average"] = round(
                lowest_group_value,
                3,
            )

            extra_numbers.update(
                [
                    round(highest_group_value, 3),
                    round(lowest_group_value, 3),
                ]
            )

            top_groups = []

            for group_name, value in grouped.head(5).items():
                top_groups.append(
                    f"{group_name}: {value:.3f}"
                )

            facts["top_groups_by_average"] = (
                "; ".join(top_groups)
            )

    return facts, extra_numbers


def insight_node(state):
    question = state.get(
        "question",
        "",
    )

    data_stats = state.get(
        "data_stats"
    )

    research_summary = state.get(
        "research_summary"
    )

    dataset_path = state.get(
        "dataset_path"
    )

    if not data_stats and not research_summary:
        return {
            "insights": [],
            "warnings": state.get(
                "warnings",
                [],
            ),
        }

    question_facts, extra_numbers = (
        _calculate_question_facts(
            question,
            dataset_path,
        )
    )

    prompt = (
        f"Question:\n{question}\n\n"
        f"Dataset statistics:\n"
        f"{_format_stats(data_stats)}\n\n"
        f"Question-specific calculated dataset facts:\n"
        f"{_format_facts(question_facts)}\n\n"
        f"Research findings:\n"
        f"{_format_claims(research_summary)}\n\n"
        "Generate the most useful insights for the question. "
        "Prioritize the question-specific facts when they directly "
        "answer what the user asked."
    )

    try:

        result = ask_json(
            prompt,
            InsightList,
            system=SYSTEM,
            temperature=0.3,
        )

    except errors.APIError as error:

        return {
            "insights": [],
            "warnings": state.get(
                "warnings",
                [],
            )
            + [
                f"Insight generation failed: {error.message}"
            ],
        }

    allowed_numbers = collect_allowed_numbers(
        data_stats,
        research_summary,
    )

    allowed_numbers.update(
        round(float(value), 3)
        for value in extra_numbers
    )

    kept = []
    discarded = 0

    for text in result.insights:

        ok, _ = validate_insight(
            text,
            allowed_numbers,
        )

        if ok:
            kept.append(text)
        else:
            discarded += 1

    warnings = state.get(
        "warnings",
        [],
    )

    if discarded:

        warnings = warnings + [
            f"{discarded} generated insight(s) discarded: "
            "contained unverified number(s)."
        ]

    return {
        "insights": kept,
        "warnings": warnings,
    }
