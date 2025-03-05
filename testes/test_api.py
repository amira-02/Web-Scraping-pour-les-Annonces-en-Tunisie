# tests/test_api.py
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_get_annonces():
    response = client.get("/annonces")
    assert response.status_code == 200
