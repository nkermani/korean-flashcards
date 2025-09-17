from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_text():
    response = client.post("/generate", json={"prompt": "Hello!"})
    assert response.status_code == 200
    assert "response" in response.json()
