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


def test_real_users(client, user, token):
    user_schema = UserPublicSchema.model_validate(user).model_dump()
    response = client.get("/users/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_schema]}


def test_get_user_by_id(client, user):
    response = client.get("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "teste",
        "email": "teste@test.com",
        "id": 1,
    }


def test_update_user(client, user, token):
    response = client.put(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
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


def test_update_integrity_error(client, user, token):
    client.post(
        "/users",
        json={
            "username": "fausto",
            "email": "fausto@exemplo.com",
            "password": "secret",
        },
    )

    resopnse_update = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "fausto",
            "email": "bob@exemplo.com",
            "password": "mynewpassword",
        },
    )

    assert resopnse_update.status_code == HTTPStatus.CONFLICT
    assert resopnse_update.json() == {"detail": "❌ Username of Email already exists!"}


def test_update_user_not_authorized(client, token):
    response = client.put(
        "/users/2",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "bob",
            "email": "bob@example.com",
            "password": "secret",
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        "detail": "❌ You do not have permission to update this user."
    }


def test_delete_user(client, user):
    response = client.delete("/users/1")
    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.content == b""


def test_delete_user_not_found(client):
    response = client.delete("/users/2")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "❌ User not found!"}


def test_get_token(client, user):
    response = client.post(
        "/token",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert "access_token" in token
