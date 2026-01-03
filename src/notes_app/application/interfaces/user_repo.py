import abc

from notes_app.domain.entities.user import User as UserEntity


class UserRepoInterface(abc.ABC):
    @abc.abstractmethod
    async def add_user(self, user: UserEntity) -> UserEntity | None:
        pass

    @abc.abstractmethod
    async def get_user_by_user_id(self, user_id: int) -> UserEntity | None:
        pass

    @abc.abstractmethod
    async def get_user_by_username(self, username: str) -> UserEntity | None:
        pass
