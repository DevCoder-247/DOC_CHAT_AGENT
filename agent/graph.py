from langgraph.graph import StateGraph
from agent.state import AgentState
from agent.nodes import (
    chunk_node,
    embed_node,
    graph_node,
    query_node,
    answer_node,
)

def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("chunk", chunk_node)
    builder.add_node("embed", embed_node)
    builder.add_node("graph_store", graph_node)
    builder.add_node("vector_search", query_node)
    builder.add_node("generate_answer", answer_node)  # ✅ FIXED

    builder.set_entry_point("chunk")

    builder.add_edge("chunk", "embed")
    builder.add_edge("embed", "graph_store")
    builder.add_edge("graph_store", "vector_search")
    builder.add_edge("vector_search", "generate_answer")

    return builder.compile()

# EXPORT
graph = build_graph()
