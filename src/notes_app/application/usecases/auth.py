from notes_app.application.exception import (
    InvalidCredentialsError,
    UsernameNotFoundError,
)
from notes_app.application.interfaces.hasher import HasherInterface
from notes_app.application.interfaces.token import TokenInterface
from notes_app.application.interfaces.user_repo import UserRepoInterface


async def login(
    username: str,
    password: str,
    user_repo: UserRepoInterface,
    hasher: HasherInterface,
    token_service: TokenInterface,
) -> dict[str, str]:
    user_from_repo = await user_repo.get_user_by_username(username=username)
    if not user_from_repo:
        raise UsernameNotFoundError()
    if not hasher.verify_password(password, user_from_repo.hashed_password):
        raise InvalidCredentialsError()
    token = token_service.create_token(user_id=user_from_repo.id)
    return {"access_token": token, "token_type": "bearer"}
