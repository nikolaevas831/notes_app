from notes_app.application.interfaces.user_repo import UserRepoInterface
from notes_app.domain.entities.user import User as UserEntity


class UserRepoMock(UserRepoInterface):
    def __init__(self) -> None:
        self.users: dict = {}
        self.users_by_username: dict = {}
        self._counter: int = 1

    async def add_user(self, user: UserEntity) -> UserEntity | None:
        if user.id is None:
            user.id = self._counter
            self._counter += 1

        self.users[user.id] = user
        self.users_by_username[user.username] = user
        return user

    async def get_user_by_user_id(self, user_id: int) -> UserEntity | None:
        return self.users.get(user_id)

    async def get_user_by_username(self, username: str) -> UserEntity | None:
        return self.users_by_username.get(username)
