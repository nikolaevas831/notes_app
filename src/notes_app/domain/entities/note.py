from dataclasses import dataclass


@dataclass
class Note:
    head: str
    body: str
    user_id: int
    id: int | None = None
