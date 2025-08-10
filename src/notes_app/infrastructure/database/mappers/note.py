from notes_app.application.dto.note import NoteDTO
from notes_app.infrastructure.database.models.note import Note as NoteORM
from notes_app.domain.entities.note import Note as NoteEntity


class NoteMapper:
    @staticmethod
    def map_note_orm_to_dto(note_orm: NoteORM) -> NoteDTO:
        return NoteDTO(
            id=note_orm.id,
            head=note_orm.head,
            body=note_orm.body,
            user_id=note_orm.user_id,
        )

    @staticmethod
    def map_note_entity_to_orm(note_entity: NoteEntity) -> NoteORM:
        return NoteORM(
            id=note_entity.id,
            head=note_entity.head,
            body=note_entity.body,
            user_id=note_entity.user_id,
        )

    @staticmethod
    def map_note_orm_to_entity(note_orm: NoteORM) -> NoteEntity:
        return NoteEntity(
            head=note_orm.head,
            body=note_orm.body,
            user_id=note_orm.user_id,
            id=note_orm.id,
        )
