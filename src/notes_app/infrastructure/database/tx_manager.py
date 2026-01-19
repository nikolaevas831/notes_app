from sqlalchemy.ext.asyncio import AsyncSession

from notes_app.application.interfaces.txmanager import TxManagerInterface


class TxManagerImlp(TxManagerInterface):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
