from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from notes_app.infrastructure.database.config import DBConfig


def build_async_engine(db_config: DBConfig) -> AsyncEngine:
    engine = create_async_engine(url=db_config.async_db_url, echo=True, echo_pool=True)
    return engine


def build_async_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    session_factory = async_sessionmaker(
        autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
    )
    return session_factory


def build_sync_engine(db_config: DBConfig) -> Engine:
    engine = create_engine(url=db_config.sync_db_url)
    return engine


def build_sync_session_factory(engine: Engine) -> sessionmaker[Session]:
    session_factory = sessionmaker(
        autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
    )
    return session_factory
