from src.agents.graph import build_graph


graph = build_graph()


def run_agent(question: str):
    result = graph.invoke({
        "question": question
    })

    return result