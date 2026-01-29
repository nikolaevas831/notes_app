from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session

from notes_app.application.interfaces.txmanager import SyncTxManagerInterface, TxManagerInterface


class TxManagerImlp(TxManagerInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()


class SyncTxManagerImpl(SyncTxManagerInterface):
    def __init__(self, session: Session) -> None:
        self._session = session

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
