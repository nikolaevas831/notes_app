from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from notes_app.application.interfaces.note_repo import NoteRepoInterface, SyncNoteRepoInterface
from notes_app.domain.entities.note import Note as NoteEntity
from notes_app.infrastructure.database.mappers.note import NoteMapper
from notes_app.infrastructure.database.models.note import Note


class NoteRepo(NoteRepoInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_note(self, entity_note: NoteEntity) -> NoteEntity:
        note_orm = NoteMapper.map_note_entity_to_orm(entity_note)
        self._session.add(note_orm)
        await self._session.flush()
        await self._session.refresh(note_orm)
        saved_entity = NoteMapper.map_note_orm_to_entity(note_orm)
        return saved_entity

    async def get_note(self, note_id: int) -> NoteEntity | None:
        stmt = select(Note).where(Note.id == note_id)
        result = await self._session.scalars(stmt)
        note: Note = result.first()
        return NoteMapper.map_note_orm_to_entity(note) if note else None

    async def get_notes(self, user_id) -> list[NoteEntity]:
        stmt = select(Note).where(Note.user_id == user_id)
        result = await self._session.scalars(stmt)
        notes: list[Note] = list(result)
        return [NoteMapper.map_note_orm_to_entity(note) for note in notes]

    async def delete_note(self, note_id: int) -> NoteEntity | None:
        stmt = select(Note).where(Note.id == note_id).limit(1)
        result = await self._session.scalars(stmt)
        note = result.first()
        if note:
            await self._session.delete(note)
            return NoteMapper.map_note_orm_to_entity(note)
        return None


class SyncNoteRepo(SyncNoteRepoInterface):
    def __init__(self, session: Session):
        self._session = session

    def delete_all_notes(self) -> None:
        self._session.query(Note).delete()
