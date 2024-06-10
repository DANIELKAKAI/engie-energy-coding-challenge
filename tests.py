import uuid

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "Azure"}


def test_add_user():
    email = f"{uuid.uuid4()}@gmail.com"
    response = client.post(
        "/users", json={"email": email, "password": "password"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["email"] == email
    assert data["is_active"] == True
    assert data["items"] == []
