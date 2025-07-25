from fastapi.testclient import TestClient
from main import app  # Replace with your FastAPI app import

client = TestClient(app)

def test_app_starts():
    response = client.get("/")
    assert response.status_code in [200, 404]  # 404 if root route doesn't exist