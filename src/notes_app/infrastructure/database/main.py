from functools import cached_property

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from notes_app.infrastructure.database.config import DBConfig


class DBConnection:
    def __init__(self, db_config: DBConfig) -> None:
        self.db_config = db_config

    @cached_property
    def async_engine(self) -> AsyncEngine:
        return create_async_engine(url=self.db_config.async_db_url, echo=True, echo_pool=True)

    @cached_property
    def async_session_factory(self) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(
            autocommit=False, autoflush=False, expire_on_commit=False, bind=self.async_engine
        )

    @cached_property
    def sync_engine(self) -> Engine:
        return create_engine(url=self.db_config.sync_db_url)

    @cached_property
    def sync_session_factory(self) -> sessionmaker[Session]:
        return sessionmaker(
            autocommit=False, autoflush=False, expire_on_commit=False, bind=self.sync_engine
        )
