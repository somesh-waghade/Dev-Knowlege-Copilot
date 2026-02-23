import random
import json
from locust import HttpUser, task, between

class RAGUser(HttpUser):
    # Simulate a user thinking between 1 and 3 seconds between queries
    wait_time = between(1, 3)
    
    def on_start(self):
        """Load the golden dataset to use for queries."""
        try:
            with open("data/golden_dataset.json", "r") as f:
                self.queries = json.load(f)
        except Exception:
            # Fallback if file not found
            self.queries = [{"query": "What is FastAPI?"}]

    @task(3)
    def query_rag(self):
        """Simulate a RAG query with bypass_llm to test retrieval speed."""
        selected = random.choice(self.queries)
        payload = {
            "query": selected["query"],
            "top_k": 5,
            "bypass_llm": True  # Bypass LLM to focus on system concurrency
        }
        self.client.post("/api/v1/query", json=payload, name="/query (bypass)")

    @task(1)
    def check_health(self):
        """Simulate a health check probe."""
        self.client.get("/api/v1/health", name="/health")

    @task(1)
    def list_docs(self):
        """Simulate browsing documents."""
        self.client.get("/api/v1/documents", name="/documents")
