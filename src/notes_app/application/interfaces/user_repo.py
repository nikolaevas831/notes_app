import abc

from notes_app.domain.entities.user import User


class UserRepoInterface(abc.ABC):
    @abc.abstractmethod
    async def add_user(self, user: User) -> User:
        pass

    @abc.abstractmethod
    async def get_user_by_user_id(self, user_id: int) -> User | None:
        pass

    @abc.abstractmethod
    async def get_user_by_username(self, username: str) -> User | None:
        pass
