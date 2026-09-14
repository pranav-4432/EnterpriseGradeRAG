import time
import logfire
from typing import List, Dict, Any
from flashrank import Ranker, RerankRequest

_ranker = None


def get_ranker():
    global _ranker
    if _ranker is None:
        try:
            logfire.info("Initializing FlashRank Model (TinyBERT) locally...")
            _ranker = Ranker()
        except Exception as e:
            logfire.warning(f"Failed to initialize FlashRank Ranker: {e}")
            _ranker = None
    return _ranker


def rerank_documents(query: str, documents: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
    """Rerank retrieved documents using FlashRank cross-encoder."""
    if not documents:
        return []

    with logfire.span("🧮 Semantic Reranking"):
        logfire.info(f"[Reranker] Sending {len(documents)} docs to FlashRank Cross-Encoder...")
        start_time = time.time()

        ranker = get_ranker()
        if ranker is None:
            return documents[:top_n]

        try:
            passages = [
                {"id": idx, "text": str(doc.get("text", "")), "meta": doc}
                for idx, doc in enumerate(documents)
            ]
            rerank_request = RerankRequest(query=query, passages=passages)
            results = ranker.rerank(rerank_request)

            reranked_docs = []
            for res in results[:top_n]:
                meta = dict(res.get("meta", {}))
                score_val = res.get("score", 0.0)
                meta["rerank_score"] = float(score_val) if score_val is not None else 0.0
                reranked_docs.append(meta)

            elapsed = time.time() - start_time
            top_score = reranked_docs[0]["rerank_score"] if reranked_docs else 0.0
            logfire.info(f"✅ [Reranker] Done in {elapsed:.2f}s. Top semantic score: {top_score}")
            logfire.info(f"Reranking complete. Top {len(reranked_docs)} passages selected.")

            return reranked_docs
        except Exception as e:
            logfire.warning(f"Reranking failed: {e}. Falling back to original documents.")
            return documents[:top_n]
