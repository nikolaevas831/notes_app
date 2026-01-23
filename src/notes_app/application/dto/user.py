from dataclasses import dataclass

from notes_app.application.dto.note import NoteDTO


@dataclass
class UserDTO:
    id: int
    username: str
    password: str
    notes: list[NoteDTO] | None


@dataclass
class CreateUserDTO:
    username: str
    password: str


@dataclass
class LoggedInUserDTO:
    access_token: str
    token_type: str
