from collections.abc import AsyncGenerator
from typing import Any

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession

from notes_app.infrastructure.config import Config
from notes_app.infrastructure.database.main import DBConnection
from notes_app.infrastructure.database.models.base import Base
from tests.mocks.note_repo import NoteRepoMock
from tests.mocks.tx_manager import TxManagerMock
from tests.mocks.user_repo import UserRepoMock


@pytest.fixture(scope="session")
def db_connection(config: Config) -> DBConnection:
    return DBConnection(db_config=config.db)


@pytest.fixture(scope="session")
def async_engine(db_connection: DBConnection) -> AsyncEngine:
    return db_connection.async_engine


@pytest.fixture(scope="session")
def async_session_factory(db_connection: DBConnection) -> async_sessionmaker[AsyncSession]:
    return db_connection.async_session_factory


@pytest.fixture
async def session(async_session_factory: async_sessionmaker) -> AsyncGenerator[AsyncSession]:
    async with async_session_factory() as session:
        yield session


@pytest.fixture(autouse=True)
async def create_tables(db_connection: DBConnection) -> AsyncGenerator[None, Any]:
    """Создаёт таблицы в тестовой БД перед всеми тестами"""
    async with db_connection.async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with db_connection.async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def tx_manager_mock() -> TxManagerMock:
    return TxManagerMock()


@pytest.fixture
def note_repo_mock() -> NoteRepoMock:
    return NoteRepoMock()


@pytest.fixture
def user_repo_mock() -> UserRepoMock:
    return UserRepoMock()
