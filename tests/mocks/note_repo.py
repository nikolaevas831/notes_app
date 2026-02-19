from notes_app.application.interfaces.note_repo import NoteRepoInterface
from notes_app.domain.entities.note import Note as NoteEntity


class NoteRepoMock(NoteRepoInterface):
    def __init__(self) -> None:
        self.notes: dict[int, NoteEntity] = {}
        self._counter: int = 1

    async def add_note(self, note: NoteEntity) -> NoteEntity:
        if note.id is None:
            note.id = self._counter
            self._counter += 1
        self.notes[note.id] = note
        return note

    async def get_note(self, note_id: int) -> NoteEntity | None:
        return self.notes.get(note_id)

    async def get_notes(self, user_id: int) -> list[NoteEntity]:
        return [note for note in self.notes.values() if note.user_id == user_id]

    async def delete_note(self, note_id: int) -> NoteEntity | None:
        return self.notes.pop(note_id, None)
