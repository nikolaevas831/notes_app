from datetime import timedelta, datetime, timezone

import jwt
from jwt import InvalidTokenError

from notes_app.application.exception import AuthError
from notes_app.application.interfaces.token import TokenInterface
from notes_app.infrastructure.auth.config import (
    AUTH_JWT_SECRET_KEY,
    AUTH_JWT_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


class JwtTokenService(TokenInterface):
    def create_token(self, user_id: int) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode = {"sub": str(user_id), "exp": expire}
        encoded_jwt_token = jwt.encode(
            payload=to_encode, key=AUTH_JWT_SECRET_KEY, algorithm=AUTH_JWT_ALGORITHM
        )
        return encoded_jwt_token

    def decode_token(self, token: str) -> int:
        try:
            payload = jwt.decode(
                jwt=token, key=AUTH_JWT_SECRET_KEY, algorithms=[AUTH_JWT_ALGORITHM]
            )
            sub = payload.get("sub")
            if sub is None:
                raise AuthError("No sub")
            return int(sub)
        except InvalidTokenError as e:
            raise AuthError("Invalid token") from e
