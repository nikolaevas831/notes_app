from notes_app.application.dto.user import CreateUserDTO, UserDTO
from notes_app.domain.entities.user import User as UserEntity


class UserMapper:
    @staticmethod
    def map_user_dto_to_entity(user_dto: CreateUserDTO, user_hashed_password: str) -> UserEntity:
        return UserEntity(username=user_dto.username, hashed_password=user_hashed_password)

    @staticmethod
    def map_user_entity_to_dto(user_entity: UserEntity) -> UserDTO:
        if user_entity.id is None:
            error_msg = "Cannot map User entity without ID to UserDTO"
            raise ValueError(error_msg)
        return UserDTO(id=user_entity.id, username=user_entity.username, notes=None)
