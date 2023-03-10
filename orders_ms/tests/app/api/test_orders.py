from starlette import status
from fastapi.testclient import TestClient

from app.web.main import app

client = TestClient(app)


def test_get_orders(test_db):
    response = client.get("/v1/orders/")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
