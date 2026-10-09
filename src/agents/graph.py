from src.agents.insight_node import insight_node
from src.agents.combine_node import combine_node
from langgraph.graph import END, StateGraph

from src.agents.data_node import data_node
from src.agents.planner_node import planner_node
from src.agents.report_node import report_node
from src.agents.research_node import research_node
from src.agents.state import AgentState


def route_after_planner(state):
    branches = []

    if state.get("needs_research"):
        branches.append("research")

    if state.get("needs_data"):
        branches.append("data")

    return branches or ["report"]


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("research", research_node)
    graph.add_node("data", data_node)
    graph.add_node("report", report_node)
    graph.add_node("insight", insight_node)   
    graph.add_node("combine", combine_node)
    graph.set_entry_point("planner")

    graph.add_conditional_edges(
        "planner",
        route_after_planner,
        ["research", "data", "report"]
    )

    graph.add_edge("research", "report")
    graph.add_edge("data", "report")
    graph.add_edge("report", "insight")
    graph.add_edge("insight", "combine")
    graph.add_edge("combine", END)
    return graph.compile()