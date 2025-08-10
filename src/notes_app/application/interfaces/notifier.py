import abc

from notes_app.application.dto.note import NoteDTO


class NotifierInterface(abc.ABC):
    @abc.abstractmethod
    async def notify_note_created(self, note: NoteDTO) -> None:
        pass

    @abc.abstractmethod
    async def notify_note_deleted(self, note: NoteDTO) -> None:
        pass
