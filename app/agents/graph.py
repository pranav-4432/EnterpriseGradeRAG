from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.agents.state import AgentState
from app.agents.nodes.planner import planner_node
from app.agents.nodes.retriever import retriever_node
from app.agents.nodes.responder import responder_node

# Build LangGraph workflow
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("planner", planner_node)
workflow.add_node("retriever", retriever_node)
workflow.add_node("responder", responder_node)

# Add Edges
workflow.add_edge(START, "planner")
workflow.add_edge("planner", "retriever")
workflow.add_edge("retriever", "responder")
workflow.add_edge("responder", END)

# In-memory checkpointer for thread_id / conversational memory
checkpointer = MemorySaver()

# Compile the agent graph
rag_agent = workflow.compile(checkpointer=checkpointer)

__all__ = ["rag_agent"]
