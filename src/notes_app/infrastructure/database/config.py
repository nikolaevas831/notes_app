from dataclasses import dataclass


@dataclass
class DBConfig:
    database_name: str
    host: str
    port: int
    user: str
    password: str
    async_driver: str = "postgresql+asyncpg"
    sync_driver: str = "postgresql"

    @property
    def async_db_url(self) -> str:
        return f"{self.async_driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_name}"

    @property
    def sync_db_url(self) -> str:
        return f"{self.sync_driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database_name}"
