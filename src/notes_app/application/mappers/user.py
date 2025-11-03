from notes_app.application.dto.user import CreateUserDTO
from notes_app.domain.entities.user import User as EntityUser


class UserMapper:
    @staticmethod
    def map_user_dto_to_entity(user_dto: CreateUserDTO, user_hashed_password: str) -> EntityUser:
        return EntityUser(username=user_dto.username, hashed_password=user_hashed_password)
