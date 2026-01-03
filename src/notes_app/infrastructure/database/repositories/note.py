from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from notes_app.application.interfaces.note_repo import NoteRepoInterface, SyncNoteRepoInterface
from notes_app.domain.entities.note import Note as NoteEntity
from notes_app.infrastructure.database.mappers.note import NoteMapper
from notes_app.infrastructure.database.models.note import Note as NoteORM


class NoteRepo(NoteRepoInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._mapper = NoteMapper()

    async def add_note(self, entity_note: NoteEntity) -> NoteEntity:
        note_orm = self._mapper.map_note_entity_to_orm(entity_note)
        self._session.add(note_orm)
        await self._session.flush()
        await self._session.refresh(note_orm)
        saved_entity = self._mapper.map_note_orm_to_entity(note_orm)
        return saved_entity

    async def get_note(self, note_id: int) -> NoteEntity | None:
        stmt = select(NoteORM).where(NoteORM.id == note_id)
        result = await self._session.scalars(stmt)
        note: NoteORM | None = result.first()
        return self._mapper.map_note_orm_to_entity(note) if note else None

    async def get_notes(self, user_id: int) -> list[NoteEntity]:
        stmt = select(NoteORM).where(NoteORM.user_id == user_id)
        result = await self._session.scalars(stmt)
        notes: list[NoteORM] = list(result)
        return [self._mapper.map_note_orm_to_entity(note) for note in notes]

    async def delete_note(self, note_id: int) -> NoteEntity | None:
        stmt = select(NoteORM).where(NoteORM.id == note_id).limit(1)
        result = await self._session.scalars(stmt)
        note: NoteORM | None = result.first()
        if note:
            await self._session.delete(note)
            return self._mapper.map_note_orm_to_entity(note)
        return None


class SyncNoteRepo(SyncNoteRepoInterface):
    def __init__(self, session: Session) -> None:
        self._session = session
        self._mapper = NoteMapper()

    def delete_all_notes(self) -> list[NoteEntity] | None:
        notes = self._session.query(NoteORM).all()
        if notes:
            mapped_notes = [self._mapper.map_note_orm_to_entity(note) for note in notes]
            self._session.query(NoteORM).delete()
            return mapped_notes
        return None
