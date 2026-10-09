import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT SETUP
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.agents.graph import build_graph


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Research Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DARK THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    html,
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {
        background-color: #0b0f14 !important;
        color: #f8fafc !important;
    }

    [data-testid="stHeader"] {
        background-color: #0b0f14 !important;
    }

    [data-testid="stToolbar"] {
        background-color: transparent !important;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }


    /* ========================================================
       ALL TEXT
       ======================================================== */

    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] label {
        color: #e5e7eb !important;
    }

    [data-testid="stMarkdownContainer"] strong {
        color: #ffffff !important;
    }

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        color: #f8fafc !important;
    }

    [data-testid="stCaptionContainer"] {
        color: #94a3b8 !important;
    }

    [data-testid="stCaptionContainer"] p {
        color: #94a3b8 !important;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background-color: #080c11 !important;
        border-right: 1px solid #1f2937;
    }

    section[data-testid="stSidebar"] * {
        color: #e5e7eb !important;
    }

    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * {
        color: #94a3b8 !important;
    }


    /* ========================================================
       TEXT AREA
       ======================================================== */

    [data-testid="stTextArea"] textarea {
        background-color: #111827 !important;
        color: #f8fafc !important;
        caret-color: #60a5fa !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }

    [data-testid="stTextArea"] textarea::placeholder {
        color: #64748b !important;
        opacity: 1 !important;
    }

    [data-testid="stTextArea"] textarea:focus {
        border-color: #60a5fa !important;
        box-shadow: 0 0 0 1px #60a5fa !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        background-color: #172033 !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        font-weight: 650 !important;
        min-height: 2.7rem;
    }

    .stButton > button:hover {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border-color: #60a5fa !important;
    }

    .stButton > button:focus {
        color: #ffffff !important;
        border-color: #60a5fa !important;
    }

    /* Primary Run Research button */

    .stButton > button[kind="primary"] {
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-color: #3b82f6 !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: #1d4ed8 !important;
        color: #ffffff !important;
        border-color: #60a5fa !important;
    }


    /* ========================================================
       LINK BUTTONS
       ======================================================== */

    [data-testid="stLinkButton"] a {
        background-color: #172033 !important;
        color: #bfdbfe !important;
        border: 1px solid #334155 !important;
        border-radius: 9px !important;
        font-weight: 600 !important;
    }

    [data-testid="stLinkButton"] a:hover {
        background-color: #1e293b !important;
        color: #ffffff !important;
        border-color: #60a5fa !important;
    }


    /* ========================================================
       METRICS
       ======================================================== */

    [data-testid="stMetric"] {
        background-color: #111827 !important;
        border: 1px solid #263241 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    [data-testid="stMetricLabel"] p {
        color: #94a3b8 !important;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }

    [data-testid="stMetricDelta"] {
        color: #93c5fd !important;
    }


    /* ========================================================
       ALERTS / INFO / SUCCESS
       ======================================================== */

    [data-testid="stAlert"] {
        background-color: #111827 !important;
        border-radius: 10px !important;
    }

    [data-testid="stAlert"] p {
        color: #e5e7eb !important;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    [data-testid="stExpander"] {
        background-color: #0f1720 !important;
        border: 1px solid #263241 !important;
        border-radius: 10px !important;
    }

    [data-testid="stExpander"] summary {
        color: #f8fafc !important;
    }

    [data-testid="stExpander"] summary p {
        color: #f8fafc !important;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color: #1f2937 !important;
    }


    /* ========================================================
       CODE
       ======================================================== */

    code {
        background-color: #111827 !important;
        color: #93c5fd !important;
    }


    /* ========================================================
       SPINNER
       ======================================================== */

    [data-testid="stSpinner"] {
        color: #bfdbfe !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# AGENT
# ============================================================

@st.cache_resource
def get_agent():
    return build_graph()


graph = get_agent()


def run_agent(question: str):
    return graph.invoke(
        {
            "question": question
        }
    )


# ============================================================
# SESSION STATE
# ============================================================

if "research_result" not in st.session_state:
    st.session_state.research_result = None

if "last_question" not in st.session_state:
    st.session_state.last_question = ""


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 AI Research Agent")

    st.caption(
        "Research • Analyze • Explain • Visualize"
    )

    if st.button(
        "＋ New Research",
        use_container_width=True,
    ):
        st.session_state.research_result = None
        st.session_state.last_question = ""
        st.rerun()

    st.divider()

    st.subheader("Agent Pipeline")

    pipeline = [
        "Understanding question",
        "Searching research sources",
        "Checking available data",
        "Analyzing dataset",
        "Generating insights",
        "Selecting visualizations",
        "Building final report",
    ]

    for item in pipeline:
        st.write(f"🔵 {item}")

    st.divider()

    st.subheader("Technology")

    st.caption("Python")
    st.caption("LangGraph")
    st.caption("Gemini")
    st.caption("Semantic Scholar")
    st.caption("Pandas")
    st.caption("Streamlit")


# ============================================================
# MAIN HEADER
# ============================================================

st.title("Ask a question. Get evidence.")

st.write(
    "An AI-powered research and data analysis agent that "
    "combines research evidence, dataset analysis, "
    "insights, and automatic visualizations."
)


# ============================================================
# QUESTION
# ============================================================

st.subheader("🔎 Research Question")

question = st.text_area(
    "Ask your research question",
    value=st.session_state.last_question,
    height=130,
    placeholder=(
        "Example: Analyze the growth of electric vehicle "
        "registrations in India from 2015 to 2022..."
    ),
    label_visibility="collapsed",
)

run_button = st.button(
    "🚀 Run Research",
    type="primary",
    use_container_width=True,
)


# ============================================================
# RUN AGENT
# ============================================================

if run_button:

    if not question.strip():

        st.warning(
            "Please enter a research question first."
        )

    else:

        st.session_state.last_question = question

        with st.spinner(
            "Research agent is working..."
        ):

            try:

                result = run_agent(question)

                st.session_state.research_result = result

            except Exception as e:

                st.error(
                    "The research agent encountered an error."
                )

                with st.expander(
                    "Technical details"
                ):
                    st.exception(e)


# ============================================================
# RESULTS
# ============================================================

result = st.session_state.research_result


if result is not None:

    # --------------------------------------------------------
    # HELPER
    # --------------------------------------------------------

    def get_value(obj, key, default=None):

        if isinstance(obj, dict):
            return obj.get(key, default)

        return getattr(
            obj,
            key,
            default,
        )


    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    research_answered = result.get(
        "research_answered",
        False,
    )

    data_used = result.get(
        "data_used",
        False,
    )

    if research_answered and data_used:
        status_text = "Research + Data Analysis Completed"
    elif data_used:
        status_text = "Data Analysis Completed"
    elif research_answered:
        status_text = "Research Completed"
    else:
        status_text = "Completed with Limited Evidence"

    st.divider()

    st.subheader("✅ Agent Status")

    st.success(status_text)


    # --------------------------------------------------------
    # QUESTION
    # --------------------------------------------------------

    st.subheader("🎯 Question")

    st.info(
        str(
            result.get(
                "question",
                st.session_state.last_question,
            )
        )
    )


    # --------------------------------------------------------
    # DATA OVERVIEW
    # --------------------------------------------------------

    st.subheader("📊 Data Overview")

    data_profile = result.get(
        "data_profile",
        {},
    )

    rows = data_profile.get(
        "rows",
        0,
    )

    columns = data_profile.get(
        "columns",
        0,
    )

    duplicate_rows = data_profile.get(
        "duplicate_rows",
        0,
    )

    missing_values = data_profile.get(
        "missing_values",
        {},
    )

    total_missing = 0

    if isinstance(
        missing_values,
        dict,
    ):

        for value in missing_values.values():

            if isinstance(
                value,
                (int, float),
            ):
                total_missing += value

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Rows",
            rows,
        )

    with col2:
        st.metric(
            "Columns",
            columns,
        )

    with col3:
        st.metric(
            "Missing Values",
            total_missing,
        )

    with col4:
        st.metric(
            "Duplicates",
            duplicate_rows,
        )


    # --------------------------------------------------------
    # RESEARCH SUMMARY
    # --------------------------------------------------------

    st.subheader("🔎 Research Summary")

    research_summary = result.get(
        "research_summary",
    )

    overview = get_value(
        research_summary,
        "overview",
    )

    if overview:

        st.info(
            str(overview)
        )

    elif research_summary:

        st.info(
            str(research_summary)
        )

    else:

        st.info(
            "No research summary was returned."
        )


    # --------------------------------------------------------
    # DATASET
    # --------------------------------------------------------

    dataset_path = result.get(
        "dataset_path",
    )

    if dataset_path:

        st.caption(
            f"Dataset used: {dataset_path}"
        )


    # --------------------------------------------------------
    # DATA ANALYSIS
    # --------------------------------------------------------

    st.subheader("📈 Data Analysis")

    data_stats = result.get(
        "data_stats",
        {},
    )

    ev_stats = data_stats.get(
        "ev_registrations",
        {},
    )

    year_stats = data_stats.get(
        "year",
        {},
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        value = ev_stats.get(
            "mean",
            "N/A",
        )

        if isinstance(
            value,
            (int, float),
        ):
            value = f"{value:,.0f}"

        st.metric(
            "Average EV Registrations",
            value,
        )

    with col2:

        value = ev_stats.get(
            "max",
            "N/A",
        )

        if isinstance(
            value,
            (int, float),
        ):
            value = f"{value:,.0f}"

        st.metric(
            "Maximum EV Registrations",
            value,
        )

    with col3:

        minimum_year = year_stats.get(
            "min",
            "N/A",
        )

        maximum_year = year_stats.get(
            "max",
            "N/A",
        )

        st.metric(
            "Dataset Year Range",
            f"{minimum_year} - {maximum_year}",
        )


    # --------------------------------------------------------
    # KEY INSIGHTS
    # --------------------------------------------------------

    st.subheader("💡 Key Insights")

    insights = result.get(
        "insights",
        [],
    )

    if insights:

        for i, insight in enumerate(
            insights,
            start=1,
        ):

            st.markdown(
                f"**Insight {i}**"
            )

            st.write(
                insight
            )

            if i < len(insights):
                st.divider()

    else:

        st.info(
            "No insights were generated."
        )


    # --------------------------------------------------------
    # VISUALIZATIONS
    # --------------------------------------------------------

    st.subheader("📊 Visualizations")

    charts = result.get(
        "charts",
        [],
    )

    if charts:

        for index, chart in enumerate(
            charts,
            start=1,
        ):

            if not isinstance(
                chart,
                dict,
            ):
                continue

            chart_path = chart.get(
                "path",
            )

            caption = chart.get(
                "caption",
                "",
            )

            chart_type = chart.get(
                "chart_type",
                "chart",
            )

            if not chart_path:
                continue

            full_path = (
                PROJECT_ROOT /
                chart_path
            )

            if full_path.exists():

                st.markdown(
                    f"### {chart_type.title()} {index}"
                )

                st.image(
                    str(full_path),
                    caption=caption,
                    use_container_width=True,
                )

            else:

                st.warning(
                    f"Chart file not found: {chart_path}"
                )

    else:

        st.info(
            "No visualizations were generated."
        )


    # --------------------------------------------------------
    # RESEARCH SOURCES
    # --------------------------------------------------------

    st.subheader("📚 Research Evidence")

    sources = result.get(
        "research_sources",
        [],
    )

    if sources:

        for source in sources:

            title = get_value(
                source,
                "title",
                "Untitled source",
            )

            year = get_value(
                source,
                "year",
                "",
            )

            url = get_value(
                source,
                "url",
                "",
            )

            st.markdown(
                f"**{title}**"
            )

            if year:
                st.caption(
                    f"Published: {year}"
                )

            if url:

                st.link_button(
                    "View Source ↗",
                    url,
                )

            st.divider()

    else:

        st.info(
            "No research sources were returned."
        )


    # --------------------------------------------------------
    # FINAL REPORT
    # --------------------------------------------------------

    final_report = result.get(
        "final_report",
        "",
    )

    if final_report:

        st.subheader("📝 Final Report")

        with st.expander(
            "Open generated research report"
        ):

            st.write(
                final_report
            )

        st.download_button(
            label="⬇️ Download Research Report",
            data=final_report,
            file_name="ai_research_report.txt",
            mime="text/plain",
            use_container_width=True,
        )


    # --------------------------------------------------------
    # DEVELOPER DETAILS
    # --------------------------------------------------------

    with st.expander(
        "Developer Details"
    ):

        st.write(
            result
        )


# ============================================================
# EMPTY STATE
# ============================================================

else:

    st.divider()

    st.subheader(
        "What this agent can do"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "**🔎 Research**\n\n"
            "Searches relevant research sources "
            "and separates evidence from assumptions."
        )

    with col2:

        st.info(
            "**📈 Analysis**\n\n"
            "Profiles datasets, calculates statistics, "
            "and generates grounded insights."
        )

    with col3:

        st.info(
            "**📊 Output**\n\n"
            "Creates visualizations and produces "
            "a structured research report."
        )
