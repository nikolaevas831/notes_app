from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from notes_app.infrastructure.config import DATABASE_URL


class Base(DeclarativeBase):
    pass


engine = create_async_engine(DATABASE_URL)

current_session = async_sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)
