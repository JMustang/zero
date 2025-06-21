from http import HTTPStatus

from jwt import decode

from zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {"test": "test"}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=ALGORITHM)

    assert decoded["test"] == "test"
    assert "exp" in decoded
    assert decoded["exp"] > 0  # Ensure expiration is a positive timestamp


def test_jwt_invalid_token(client):
    response = client.delete(
        "/users/1", headers={"Authorization": "Bearer token-invalido"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        "detail": "❌ Could not validate credentials",
    }
