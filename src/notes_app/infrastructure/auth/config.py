from dataclasses import dataclass


@dataclass(frozen=True)
class AuthConfig:
    secret_token: str
    algorithm: str
    access_token_expire_minutes: int
