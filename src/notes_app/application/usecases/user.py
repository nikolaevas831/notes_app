from notes_app.application.dto.user import CreateUserDTO
from notes_app.application.interfaces.hasher import HasherInterface
from notes_app.application.interfaces.txmanager import TxManagerInterface
from notes_app.application.interfaces.user_repo import UserRepoInterface


from notes_app.application.exception import UsernameAlreadyExistsError
from notes_app.application.mappers.user import UserMapper
from notes_app.domain.entities.user import User as EntityUser


async def create_user(
    user_data: CreateUserDTO,
    user_repo: UserRepoInterface,
    tx_manager: TxManagerInterface,
    hasher: HasherInterface,
) -> EntityUser:
    username_exists_check = await user_repo.get_user_by_username(
        username=user_data.username
    )
    if username_exists_check:
        raise UsernameAlreadyExistsError()
    hashed_password = hasher.hash_password(password=user_data.password)
    user = UserMapper.map_user_dto_to_entity(user_data, hashed_password)
    created_user = await user_repo.add_user(user)
    await tx_manager.commit()
    return created_user
