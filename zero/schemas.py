from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    Message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublicSchema(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
