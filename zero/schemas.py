from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublicSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True, extra="forbid")


class UserList(BaseModel):
    users: list[UserPublicSchema]


class Token(BaseModel):
    access_token: str
    token_type: str
