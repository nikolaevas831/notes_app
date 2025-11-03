from dataclasses import dataclass


@dataclass
class User:
    username: str
    hashed_password: str
    id: int | None = None
