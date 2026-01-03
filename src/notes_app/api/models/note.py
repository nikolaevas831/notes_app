from pydantic import BaseModel


class NoteSchema(BaseModel):
    id: int
    head: str
    body: str
    user_id: int


class NoteCreateSchema(BaseModel):
    head: str
    body: str


class NoteResponseSchema(BaseModel):
    id: int
    user_id: int
    head: str
    body: str | None
