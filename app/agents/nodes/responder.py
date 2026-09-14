import logfire
from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.state import AgentState
from app.agents.nodes.planner import get_llm


def responder_node(state: AgentState) -> dict:
    query = state.get("current_query", "")
    documents = state.get("documents", [])
    plan = list(state.get("plan", []))

    context_blocks = []
    for idx, doc in enumerate(documents, start=1):
        source = doc.get("source", "Unknown")
        text = doc.get("text", "")
        context_blocks.append(f"Document {idx} (Source: {source}):\n{text}")

    context_str = "\n\n---\n\n".join(context_blocks) if context_blocks else "No relevant context found."

    system_prompt = (
        "You are an enterprise AI assistant with access to verified company documentation.\n"
        "Your task is to provide accurate, concise, and helpful answers based ONLY on the provided context.\n"
        "If the context does not contain enough information to answer the question, clearly state that the information is not available.\n"
        "Always cite sources where applicable."
    )

    user_prompt = f"Context:\n{context_str}\n\nUser Question: {query}\n\nAnswer:"

    final_answer = ""
    with logfire.span("✍️ LLM Synthesis"):
        logfire.info("Generating technical RAG response...")
        try:
            llm = get_llm()
            response = llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ])
            final_answer = response.content if hasattr(response, "content") else str(response)
            logfire.info("✅ Response synthesised via LLM.")
            plan.append("Synthesizing final answer grounded in retrieved context")
        except Exception as e:
            logfire.error(f"Responder node generation error: {e}")
            final_answer = "I apologize, but I encountered an error while generating the response."

    return {
        "final_answer": final_answer,
        "plan": plan,
        "status": "Completed",
    }
