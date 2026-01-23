from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: str


class RegisterUserResponseSchema(BaseModel):
    username: str


class LoggedInUserResponseSchema(BaseModel):
    access_token: str
    token_type: str
