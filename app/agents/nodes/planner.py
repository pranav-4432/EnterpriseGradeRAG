import logfire
from app.agents.state import AgentState
from app.config import settings


def get_llm():
    if settings.GEMINI_API_KEY:
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.0,
        )
    elif settings.GROQ_API_KEY:
        from langchain_groq import ChatGroq
        return ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL,
            temperature=0.0,
        )
    raise ValueError("No LLM API key configured in settings")


def planner_node(state: AgentState) -> dict:
    query = state.get("current_query", "")
    plan = list(state.get("plan", []))

    with logfire.span("🧠 Planner Decision"):
        logfire.info('Intent identified: "{query}"', query=query)
        plan.append(f'Intent identified: "{query}"')

    return {
        "plan": plan,
        "status": "Planning complete",
    }
