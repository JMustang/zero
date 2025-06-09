from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from zero.database import get_session
from zero.models import User
from zero.schemas import Message, UserList, UserPublicSchema, UserSchema

app = FastAPI(
    title='Test for Zero API',
    description='Treinamento com python e FastAPI. Ministrado por dunossauro',
    version='0.1.0',
)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read():
    return {'message': 'Test API'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublicSchema)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where((User.username == user.username) | (User.email == user.email))
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='❌ Username already exists!'
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail='❌ Email already exists!'
            )
    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def list_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.get('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublicSchema)
def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='❌ User not found!')

    return db_user


@app.put('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublicSchema)
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='❌ User not found!')
    user_db.username = user.username
    user_db.password = user.password
    user_db.email = user.email
    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@app.delete('/users/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))
    if not user_db:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='❌ User not found!')
    session.delete(user_db)
    session.commit()
    return {'message': '✅ User deleted successfully'}
