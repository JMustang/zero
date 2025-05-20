from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from zero.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_app(client):
    # Act
    response = client.get('/')

    # Assert
    assert response.json() == {'message': 'Test API'}
    assert response.status_code == HTTPStatus.OK


def test_create_user(client):
    response = client.post(
        '/users/',
        json={'username': 'alice', 'email': 'alice@exemple.com', 'password': 'secret'},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'alice',
        'email': 'alice@exemple.com',
    }
