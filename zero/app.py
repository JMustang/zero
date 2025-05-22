from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from zero.schemas import Message, UserDB, UserList, UserPublicSchema, UserSchema

# Banco local para testes
database = []

app = FastAPI(
    title="Test for Zero API",
    description="Treinamento com python e FastAPI. Ministrado por dunossauro",
    version="0.1.0",
)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read():
    return {"message": "Test API"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublicSchema)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id


@app.get("/users/", status_code=HTTPStatus.OK, response_model=UserList)
def list_users():
    return {"users": database}


@app.put("/users/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublicSchema)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=user_id)

    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="❌ User not found!"
        )
    database[user_id - 1] = user_with_id
    return user_with_id
