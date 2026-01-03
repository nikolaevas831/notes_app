from datetime import UTC, datetime, timedelta

import jwt
from jwt import InvalidTokenError

from notes_app.application.exception import AuthError
from notes_app.application.interfaces.token import TokenInterface
from notes_app.infrastructure.auth.config import AuthConfig


class JwtTokenService(TokenInterface):
    def __init__(self, auth_config: AuthConfig) -> None:
        self._auth_config = auth_config

    def create_token(self, user_id: int) -> str:
        expire = datetime.now(UTC) + timedelta(
            minutes=self._auth_config.access_token_expire_minutes
        )
        to_encode = {"sub": str(user_id), "exp": expire}
        encoded_jwt_token = jwt.encode(
            payload=to_encode,
            key=self._auth_config.secret_token,
            algorithm=self._auth_config.algorithm,
        )
        return encoded_jwt_token

    def decode_token(self, token: str) -> int:
        try:
            payload = jwt.decode(
                jwt=token,
                key=self._auth_config.secret_token,
                algorithms=self._auth_config.algorithm,
            )
            sub = payload.get("sub")
            if sub is None:
                error_msg = "No sub"
                raise AuthError(error_msg)
            return int(sub)
        except InvalidTokenError as e:
            error_msg = "Invalid token"
            raise AuthError(error_msg) from e
