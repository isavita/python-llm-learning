import pytest

from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_status_endpoint(client):
    response = client.get("/status")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Ollama RAG Embeddings"
    assert response.content_type == "text/plain; charset=utf-8"
