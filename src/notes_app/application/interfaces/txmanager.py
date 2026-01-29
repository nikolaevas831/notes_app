import abc


class TxManagerInterface(abc.ABC):
    @abc.abstractmethod
    async def commit(self) -> None:
        pass

    @abc.abstractmethod
    async def rollback(self) -> None:
        pass


class SyncTxManagerInterface(abc.ABC):
    @abc.abstractmethod
    def commit(self) -> None:
        pass

    @abc.abstractmethod
    def rollback(self) -> None:
        pass
