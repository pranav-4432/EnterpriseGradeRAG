from typing import TypedDict, List, Dict, Any, Optional


class AgentState(TypedDict, total=False):
    messages: List[Dict[str, Any]]
    current_query: str
    plan: List[str]
    documents: List[Dict[str, Any]]
    status: str
    final_answer: Optional[str]
