from http import HTTPStatus

from fastapi.testclient import TestClient

from zero.app import app


def test_app():
    client = TestClient(app)

    # Act
    response = client.get("/")

    # Assert
    assert response.json() == {"message": "Test API"}
    assert response.status_code == HTTPStatus.OK


def test_create_user():
    client = TestClient(app)
    response = client.post(
        "/users/",
        json={"username": "alice", "email": "alice@exemple.com", "password": "secret"},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "alice",
        "email": "alice@exemple.com",
    }
