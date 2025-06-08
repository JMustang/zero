from http import HTTPStatus

from zero.schemas import UserPublicSchema


def test_app(client):
    # Act
    response = client.get("/")

    # Assert
    assert response.json() == {"message": "Test API"}
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    response = client.post(
        "/users/",
        json={"username": "alice", "email": "alice@example.com", "password": "secret"},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "alice",
        "email": "alice@example.com",
    }


def test_read_users(client, user):
    # Act
    response = client.get("/users/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "id": 1,
                "username": "teste",
                "email": "teste@test.com",
                # "password": "teste",
            }
        ]
    }


def test_real_users_with_users(client, user):
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    response = client.get("/users/")
    assert response.json() == {"users": [user_schema]}


def test_get_user_by_id(client):
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "alice",
        "email": "alice@example.com",
        "id": 1,
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "bob",
        "email": "bob@example.com",
        "id": 1,
    }


def test_update_user_not_found(client):
    response = client.put(
        "/users/2",
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "❌ User not found!"}


def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.content == b""


def test_delete_user_not_found(client):
    response = client.delete("/users/2")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "❌ User not found!"}
