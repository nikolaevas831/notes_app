from dataclasses import dataclass


@dataclass
class NoteDTO:
    id: int
    head: str
    body: str | None
    user_id: int


@dataclass
class CreateNoteDTO:
    head: str
    body: str | None
    user_id: int
