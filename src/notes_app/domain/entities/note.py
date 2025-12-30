from dataclasses import dataclass


@dataclass
class Note:
    head: str
    body: str | None
    user_id: int
    id: int | None = None
