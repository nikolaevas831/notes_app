import abc


class HasherInterface(abc.ABC):
    @abc.abstractmethod
    def hash_password(self, password: str) -> str:
        pass

    @abc.abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        pass
