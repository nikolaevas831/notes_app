from notes_app.application.dto.user import UserDTO
from notes_app.infrastructure.database.mappers.note import NoteMapper
from notes_app.infrastructure.database.models.user import User as UserORM
from notes_app.domain.entities.user import User as UserEntity


class UserMapper:
    @staticmethod
    def map_user_orm_to_dto(user_orm: UserORM) -> UserDTO:
        return UserDTO(
            id=user_orm.id,
            username=user_orm.username,
            notes=[NoteMapper.map_note_orm_to_dto(note) for note in user_orm.notes],
        )

    def map_user_entity_to_orm(user_entity: UserEntity) -> UserORM:
        return UserORM(
            username=user_entity.username, password=user_entity.hashed_password
        )

    def map_user_orm_to_entity(user_orm: UserORM) -> UserEntity:
        return UserEntity(
            id=user_orm.id,
            username=user_orm.username,
            hashed_password=user_orm.password,
        )
