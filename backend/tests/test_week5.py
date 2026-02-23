import pytest
import asyncio
from backend.retrieval.reranker import Reranker
from backend.scoring.engine import compute_confidence
from backend.generation.llm import verify_factuality

@pytest.fixture
def reranker():
    # Use a tiny model for tests if possible, or just the default
    return Reranker()

def test_compute_confidence_rerank():
    # High confidence: scores > -7.0
    assert compute_confidence([-6.5, -8.0], mode="rerank") == "high"
    # Medium confidence: scores > -10.0
    assert compute_confidence([-9.0, -11.0], mode="rerank") == "medium"
    # Low confidence: scores <= -10.0
    assert compute_confidence([-11.0, -12.0], mode="rerank") == "low"

def test_reranker_logic(reranker):
    query = "test query"
    chunks = [
        {"text": "this is irrelevant", "id": 1},
        {"text": "this is the test query answer", "id": 2},
    ]
    # We can't easily assert the exact scores without the model, 
    # but we can check the rerank() structure.
    results = reranker.rerank(query, chunks, top_n=1)
    assert len(results) == 1
    assert "rerank_score" in results[0]

@pytest.mark.asyncio
async def test_verify_factuality_mock(monkeypatch):
    # Mocking the HTTP call to verify_factuality if needed, 
    # but here we test the logic around context building.
    query = "What is FAISS?"
    answer = "FAISS is a library."
    chunks = [{"text": "FAISS is a library for similarity search."}]
    
    # This is an integration test essentially. 
    # For a true unit test, we'd mock the httpx client.
    # Given the environment, we'll just check if it runs or mock it.
    
    async def mock_post(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self): pass
            def json(self): return {
                "choices": [{"message": {"content": '{"score": 10, "is_grounded": true, "reason": "Match"}'}}],
                "usage": {"total_tokens": 50}
            }
        return MockResponse()

    import httpx
    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)
    
    result = await verify_factuality(query, answer, chunks)
    assert result["is_grounded"] is True
    assert result["factuality_score"] == 10
