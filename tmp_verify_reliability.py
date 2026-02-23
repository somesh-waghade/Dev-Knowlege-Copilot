import requests
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_health():
    print("--- Testing /health ---")
    r = requests.get(f"{BASE_URL}/health")
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")

def test_rate_limit():
    print("\n--- Testing Rate Limit (20/min) ---")
    for i in range(25):
        r = requests.post(f"{BASE_URL}/query", json={"query": "test", "bypass_llm": True})
        if r.status_code == 429:
            print(f"Hit rate limit at request {i+1}!")
            return
        elif r.status_code != 200:
            print(f"Error at request {i+1}: {r.status_code} - {r.text}")
            return
    print("Did not hit rate limit (Expected to hit at 21st request)")

if __name__ == "__main__":
    test_health()
    test_rate_limit()
