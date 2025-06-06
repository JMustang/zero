from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from zero.database import get_session
from zero.models import User
from zero.schemas import Message, UserDB, UserList, UserPublicSchema, UserSchema

# Banco local para testes
database = []

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
def get_user_by_id(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='❌ User not found!')
    return database[user_id - 1]


@app.put('/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublicSchema)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=user_id)

    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='❌ User not found!')
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='❌ User not found!')
    del database[user_id - 1]
