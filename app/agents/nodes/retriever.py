import logfire
from qdrant_client import QdrantClient
from app.config import settings
from app.services.retrieval.embeddings import embed_query
from app.services.retrieval.ranking_service import rerank_documents
from app.agents.state import AgentState

_qdrant_client = None


def get_qdrant_client():
    global _qdrant_client
    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )
    return _qdrant_client


def retriever_node(state: AgentState) -> dict:
    query = state.get("current_query", "")
    plan = list(state.get("plan", []))

    documents = []
    with logfire.span("🔍 Knowledge Retrieval"):
        logfire.info('Searching Qdrant for: "{query}"', query=query)
        try:
            query_vector = embed_query(query)
            client = get_qdrant_client()

            limit = 15
            if hasattr(client, "query_points"):
                response = client.query_points(
                    collection_name=settings.QDRANT_COLLECTION,
                    query=query_vector,
                    limit=limit,
                )
                hits = response.points if hasattr(response, "points") else response
            else:
                hits = client.search(
                    collection_name=settings.QDRANT_COLLECTION,
                    query_vector=query_vector,
                    limit=limit,
                )

            raw_docs = []
            for hit in hits:
                payload = getattr(hit, "payload", {}) or {}
                score = getattr(hit, "score", 0.0)
                raw_docs.append({
                    "text": str(payload.get("text", "")),
                    "source": str(payload.get("source", "Unknown")),
                    "source_type": str(payload.get("source_type", "Unknown")),
                    "score": float(score) if score is not None else 0.0,
                })

            logfire.info(f"Retrieved {len(raw_docs)} candidates from Vector DB")

            documents = rerank_documents(query=query, documents=raw_docs, top_n=5)
            plan.append("Retrieving relevant context from vector database")
        except Exception as e:
            logfire.error(f"Retriever node error: {e}")

    return {
        "documents": documents,
        "plan": plan,
        "status": "Context retrieved successfully",
    }
