import logging

from sqlalchemy import log as sa_log

from notes_app.infrastructure.logging.config import LoggingConfig


def setup_logging(config: LoggingConfig) -> None:
    sa_log._add_default_handler = lambda logger: None  # noqa: SLF001
    logging.getLogger("python_multipart").setLevel(logging.WARNING)
    logging.basicConfig(
        level=config.level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
