from pydantic import BaseModel


class NotePydantic(BaseModel):
    id: int
    head: str
    body: str
