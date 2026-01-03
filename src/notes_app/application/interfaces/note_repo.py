import abc

from notes_app.domain.entities.note import Note as NoteEntity


class NoteRepoInterface(abc.ABC):
    @abc.abstractmethod
    async def add_note(self, note: NoteEntity) -> NoteEntity:
        pass

    @abc.abstractmethod
    async def get_note(self, note_id: int) -> NoteEntity | None:
        pass

    @abc.abstractmethod
    async def get_notes(self, user_id: int) -> list[NoteEntity]:
        pass

    @abc.abstractmethod
    async def delete_note(self, note_id: int) -> NoteEntity | None:
        pass


class SyncNoteRepoInterface(abc.ABC):
    @abc.abstractmethod
    def delete_all_notes(self) -> list[NoteEntity] | None:
        pass
