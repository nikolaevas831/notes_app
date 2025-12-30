
from dataclasses import dataclass


@dataclass(frozen=True)
class APIConfig:
        host: str = "0.0.0.0"
        port: int = 8000
