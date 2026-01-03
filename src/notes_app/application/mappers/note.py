from notes_app.application.dto.note import NoteDTO
from notes_app.domain.entities.note import Note as NoteEntity


class NoteMapper:
    @staticmethod
    def map_note_dto_to_entity(note_dto: NoteDTO) -> NoteEntity:
        return NoteEntity(
            id=note_dto.id,
            head=note_dto.head,
            body=note_dto.body,
            user_id=note_dto.user_id,
        )

    @staticmethod
    def map_note_entity_to_dto(note_entity: NoteEntity) -> NoteDTO:
        if note_entity.id is None:
            error_msg = "Note entity must have an id"
            raise ValueError(error_msg)
        return NoteDTO(
            id=note_entity.id,
            head=note_entity.head,
            body=note_entity.body,
            user_id=note_entity.user_id,
        )
