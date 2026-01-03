from notes_app.application.dto.user import CreateUserDTO, UserDTO
from notes_app.application.exception import UsernameAlreadyExistsError
from notes_app.application.interfaces.hasher import HasherInterface
from notes_app.application.interfaces.txmanager import TxManagerInterface
from notes_app.application.interfaces.user_repo import UserRepoInterface
from notes_app.application.mappers.user import UserMapper


async def create_user(
    user_data: CreateUserDTO,
    user_repo: UserRepoInterface,
    tx_manager: TxManagerInterface,
    hasher: HasherInterface,
) -> UserDTO:
    username_exists_check = await user_repo.get_user_by_username(username=user_data.username)
    if username_exists_check:
        raise UsernameAlreadyExistsError
    hashed_password = hasher.hash_password(password=user_data.password)
    user = UserMapper.map_user_dto_to_entity(user_data, hashed_password)
    created_user_entity = await user_repo.add_user(user)
    if created_user_entity is None:
        error_msg = "Failed to create user"
        raise ValueError(error_msg)
    if created_user_entity.id is None:
        error_msg = "Created user must have an ID"
        raise ValueError(error_msg)
    await tx_manager.commit()
    return UserMapper.map_user_entity_to_dto(user_entity=created_user_entity)
