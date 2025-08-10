from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from notes_app.application.interfaces.user_repo import UserRepoInterface
from notes_app.domain.entities.user import User as UserEntity
from notes_app.infrastructure.database.mappers.user import UserMapper
from notes_app.infrastructure.database.models.user import User


class UserRepo(UserRepoInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_user(self, user: UserEntity) -> User | None:
        user_orm = UserMapper.map_user_entity_to_orm(user)
        self._session.add(user_orm)
        await self._session.flush()
        await self._session.refresh(user_orm)
        return UserMapper.map_user_orm_to_entity(user_orm)

    async def get_user_by_user_id(self, user_id: int) -> UserEntity | None:
        stmt = select(User).where(User.id == user_id)
        result = await self._session.scalars(stmt)
        user_orm = result.first()
        if not user_orm:
            return None
        user_entity = UserMapper.map_user_orm_to_entity(user_orm)
        return user_entity

    async def get_user_by_username(self, username: str) -> UserEntity | None:
        stmt = select(User).where(User.username == username)
        result = await self._session.scalars(stmt)
        user_orm = result.first()
        if not user_orm:
            return None
        user_entity = UserMapper.map_user_orm_to_entity(user_orm)
        return user_entity
