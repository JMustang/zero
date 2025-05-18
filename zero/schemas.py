from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    Message: str


class UserPublicSchema(BaseModel):
    username: str
    email: EmailStr
    id: int

    class Config:
        orm_mode = True


class UserSchema(UserPublicSchema):
    password: str


class UserDB(UserSchema):
    id: int
