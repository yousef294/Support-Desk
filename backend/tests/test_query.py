from fastapi.testclient import TestClient

from app.main import app


class FakeRetrieval:
    ready = True

    def retrieve(self, question, top_k=None):
        return [{
            "text": "Items can be returned within 30 days of delivery.",
            "metadata": {"source": "FAQs.pdf", "page": 3},
            "distance": 0.12,
        }]


class FakeGeneration:
    def generate(self, question, chunks):
        return "Items can be returned within 30 days of delivery.", ["FAQs.pdf (Pg. 3)"]


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_query_happy_path():
    with TestClient(app) as client:
        # Replace the real services with fakes so the test is deterministic
        client.app.state.retrieval = FakeRetrieval()
        client.app.state.generation = FakeGeneration()

        response = client.post("/query", json={"question": "What is the return window?"})
        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Items can be returned within 30 days of delivery."
        assert data["sources"] == ["FAQs.pdf (Pg. 3)"]


def test_query_blank_question_rejected():
    with TestClient(app) as client:
        response = client.post("/query", json={"question": "   "})
        assert response.status_code == 422


def test_query_missing_question_rejected():
    with TestClient(app) as client:
        response = client.post("/query", json={})
        assert response.status_code == 422