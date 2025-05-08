from pydantic import BaseModel


class Note(BaseModel):
    id: int
    head: str
    body: str
    model_config = {
        "from_attributes": True
    }
