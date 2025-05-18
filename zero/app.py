from http import HTTPStatus

from fastapi import FastAPI

from zero.schemas import Message, UserSchema, UserPublicSchema

app = FastAPI(title="Test for Zero API", description="FastAPI", version="0.1.0")


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read():
    return {"msg": "Test API"}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublicSchema)
def create_user(user: UserSchema):
    return user
