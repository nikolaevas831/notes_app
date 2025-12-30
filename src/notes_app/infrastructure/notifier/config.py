from dataclasses import dataclass


@dataclass(frozen=True)
class NotifierConfig:
    bootstrap_servers: str



