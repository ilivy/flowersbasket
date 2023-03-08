from starlette import status
from fastapi.testclient import TestClient

from app.web.main import app

client = TestClient(app)


def test_register(test_db):
    payload = {
        "username": "testuser",
        "email": "test@test.com",
        "password": "testuser",
        "password_confirm": "testuser",
    }
    response = client.post("/v1/register/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == payload["username"]
    assert response.json()["email"] == payload["email"]


def test_register_not_unique(test_db):
    payload = {
        "username": "testuser",
        "email": "test@test.com",
        "password": "testuser",
        "password_confirm": "testuser",
    }
    response = client.post("/v1/register/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
