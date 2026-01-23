from notes_app.application.interfaces.txmanager import TxManagerInterface


class TxManagerMock(TxManagerInterface):
    def __init__(self) -> None:
        self.committed = False
        self.rolled_back = False

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True
