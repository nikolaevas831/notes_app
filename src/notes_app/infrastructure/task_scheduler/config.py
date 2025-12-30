from dataclasses import dataclass


@dataclass(frozen=True)
class TaskSchedulerConfig:
    host: str
    port: int
    password: str
    timezone: str = "UTC"

    @property
    def broker_url(self) -> str:
        return f"redis://:{self.password}@{self.host}:{self.port}/0"

    @property
    def backend_url(self) -> str:
        return f"redis://:{self.password}@{self.host}:{self.port}/0"
