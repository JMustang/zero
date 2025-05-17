from http import HTTPStatus

from fastapi import FastAPI

from zero.schemas import Message

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read():
    return {"msg": "Test API"}
