from zero.models import User


def test_create_user(session):
    user = User(username='testuser', email='test@example.com', password='secret')

    assert user.username == 'testuser'
