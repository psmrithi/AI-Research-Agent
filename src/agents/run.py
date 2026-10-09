from src.agents.dashboard_model import build_dashboard_data
from src.agents.graph import build_graph
from src.agents.models import UnifiedAnalysis

_app = None


def get_app():
    global _app
    if _app is None:
        _app = build_graph()
    return _app


def run_analysis(question):
    """The one function the UI needs to call."""
    final_state = get_app().invoke({"question": question})
    unified = UnifiedAnalysis(**final_state["unified_analysis"])
    return build_dashboard_data(unified)