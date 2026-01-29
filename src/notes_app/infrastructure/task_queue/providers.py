from collections.abc import Iterator

from dishka import Container, Provider, Scope, from_context, make_container, provide
from sqlalchemy import Engine
from sqlalchemy.orm.session import Session, sessionmaker

from notes_app.infrastructure.config import Config
from notes_app.infrastructure.database.config import DBConfig
from notes_app.infrastructure.database.main import DBConnection
from notes_app.infrastructure.database.repositories.note import SyncNoteRepo
from notes_app.infrastructure.database.tx_manager import SyncTxManagerImpl


class ConfigProvider(Provider):
    scope = Scope.APP
    config = from_context(Config)

    @provide(scope=Scope.APP)
    def get_db_config(self, config: Config) -> DBConfig:
        return config.db


class DBProvider(Provider):
    @provide(scope=Scope.APP)
    def get_db_connection(self, db_config: DBConfig) -> DBConnection:
        return DBConnection(db_config=db_config)

    @provide(scope=Scope.APP)
    def get_sync_engine(self, db_connection: DBConnection) -> Engine:
        return db_connection.sync_engine

    @provide(scope=Scope.APP)
    def get_sync_session_factory(self, db_connection: DBConnection) -> sessionmaker[Session]:
        return db_connection.sync_session_factory

    @provide(scope=Scope.REQUEST)
    def get_db_session(self, session_factory: sessionmaker[Session]) -> Iterator[Session]:
        with session_factory() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_sync_tx_manager(self, session: Session) -> SyncTxManagerImpl:
        return SyncTxManagerImpl(session=session)

    @provide(scope=Scope.REQUEST)
    def get_note_repo(self, session: Session) -> SyncNoteRepo:
        return SyncNoteRepo(session)


def setup_di_container(context: dict[object, object]) -> Container:
    container = make_container(ConfigProvider(), DBProvider(), context=context)
    return container
