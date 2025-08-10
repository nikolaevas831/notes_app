from dataclasses import dataclass

from notes_app.application.dto.note import NoteDTO


@dataclass
class UserDTO:
    id: int
    username: str
    notes: list[NoteDTO]


@dataclass
class CreateUserDTO:
    username: str
    password: str
