import abc


class TokenInterface(abc.ABC):
    @abc.abstractmethod
    def create_token(self, user_id: int) -> str:
        pass

    @abc.abstractmethod
    def decode_token(self, token: str) -> int:
        pass
