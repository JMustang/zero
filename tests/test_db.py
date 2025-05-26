from sqlalchemy import select

from zero.models import User


def test_create_user(session):
    new_user = User(username='testuser', email='test@example.com', password='secret')

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'testuser'))
    assert user.username == 'testuser'
