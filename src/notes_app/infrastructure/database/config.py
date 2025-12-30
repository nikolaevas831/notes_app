from dataclasses import dataclass


@dataclass
class DBConfig:
    database: str
    user: str
    password: str

    @property
    def async_db_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@postgres:5432/{self.database}"

    @property
    def sync_db_url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@postgres:5432/{self.database}"
