import abc

from notes_app.application.dto.note import CreateNoteDTO
from notes_app.domain.entities.note import Note


class NoteRepoInterface(abc.ABC):
    @abc.abstractmethod
    async def add_note(self, note: CreateNoteDTO) -> Note:
        pass

    @abc.abstractmethod
    async def get_note(self, note_id: int) -> Note | None:
        pass

    @abc.abstractmethod
    async def get_notes(self, user_id: int) -> list[Note]:
        pass

    @abc.abstractmethod
    async def delete_note(self, note_id: int) -> Note | None:
        pass

class SyncNoteRepoInterface(abc.ABC):
    @abc.abstractmethod
    def delete_all_notes(self):
        pass