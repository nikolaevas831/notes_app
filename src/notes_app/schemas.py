from pydantic import BaseModel


class NotePydantic(BaseModel):
    id: int
    head: str
    body: str
    user_id: int

class NoteCreateSchema(BaseModel):
    head: str
    body: str

class UserPydantic(BaseModel):
    username: str
    password: str
