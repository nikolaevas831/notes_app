from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from notes_app.infrastructure.config import ASYNC_DATABASE_URL, SYNC_DATABASE_URL


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(ASYNC_DATABASE_URL)

async_current_session = async_sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=async_engine
)

sync_engine = create_engine(SYNC_DATABASE_URL)

sync_current_session = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=sync_engine)