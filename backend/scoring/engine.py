"""
backend/scoring/engine.py
───────────────────────────
Centralized logic for search scoring and confidence estimation.
"""

def compute_confidence(scores: list[float], mode: str = "hybrid") -> str:
    """
    Calculate confidence level based on retrieval scores.
    
    Confidence Levels:
      - HIGH:   Very strong match in top results
      - MEDIUM: Likely relevant but less certain
      - LOW:    Weak match or no results
    """
    if not scores:
        return "low"
        
    top_score = max(scores)
    
    # Thresholds for Cross-Encoder (rerank_score)
    # Calibrated for ms-marco-MiniLM-L-6-v2 based on debug output.
    # High: > -7.0
    # Medium: > -10.0
    if mode == "rerank":
        if top_score > -7.0: return "high"
        if top_score > -10.0: return "medium"
        return "low"
        
    # Thresholds for Hybrid (RRF)
    if mode == "hybrid":
        if top_score > 0.03: return "high"
        if top_score > 0.01: return "medium"
        return "low"

    # Thresholds for Vector only
    if mode == "vector":
        if top_score > 0.80: return "high"
        if top_score > 0.60: return "medium"
        return "low"

    return "low"
