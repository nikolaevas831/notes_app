from notes_app.application.interfaces.token import TokenInterface


class TokenServiceMock(TokenInterface):
    def __init__(self) -> None:
        self._tokens: dict = {}

    def create_token(self, user_id: int) -> str:
        token = f"token_{user_id}"
        self._tokens[token] = user_id
        return token

    def decode_token(self, token: str) -> int:
        if token not in self._tokens:
            msg = "Invalid token"
            raise ValueError(msg)
        return self._tokens[token]
