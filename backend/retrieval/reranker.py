"""
backend/retrieval/reranker.py
──────────────────────────────
Two-stage retrieval: Re-ranks top-K results using a Cross-Encoder.

Vector/Hybrid search is "Bi-Encoder" (fast but less accurate).
Cross-Encoders are slower but MUCH more accurate at judging 
the relationship between a specific query and a specific chunk.
"""

import threading
from sentence_transformers import CrossEncoder
from backend.core.config import settings

class Reranker:
    """
    Two-stage retrieval re-ranker using a Cross-Encoder.
    Optimized with lazy loading to save memory at startup.
    """
    def __init__(self, model_name="cross-encoder/ms-marco-TinyBERT-L-2-v2"):
        self.model_name = model_name
        self._model = None
        self._lock = threading.Lock()

    @property
    def model(self):
        if self._model is None:
            with self._lock:
                if self._model is None:  # Double-check
                    print(f"[Reranker] Loading {self.model_name}...")
                    self._model = CrossEncoder(self.model_name)
        return self._model

    def rerank(self, query: str, chunks: list[dict], top_n: int = 5) -> list[dict]:
        """
        Re-score a list of chunks based on their semantic relevance to the query.
        """
        if not chunks:
            return []

        # Prepare pairs for the Cross-Encoder: [query, text]
        pairs = [[query, c["text"]] for c in chunks]
        
        # Predict relevance scores
        scores = self.model.predict(pairs)
        
        # Attach scores to chunks
        for i, chunk in enumerate(chunks):
            chunk["rerank_score"] = float(scores[i])
            
        # Sort by rerank_score descending
        ranked_chunks = sorted(chunks, key=lambda x: x["rerank_score"], reverse=True)
        
        return ranked_chunks[:top_n]

# Singleton instance
reranker = Reranker()
