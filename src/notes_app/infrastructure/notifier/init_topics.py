import asyncio
from logging import getLogger

from notes_app.infrastructure.config import Config, load_config
from notes_app.infrastructure.logging.main import setup_logging
from notes_app.infrastructure.notifier.main import create_kafka_admin_client
from notes_app.infrastructure.notifier.topic_manager import NotifierTopicBuilder

logger = getLogger(__name__)


async def init_notifier_topics(config: Config) -> None:
    setup_logging(config=config.logging)
    admin_client = create_kafka_admin_client(config.notifier)
    builder = NotifierTopicBuilder(notifier_config=config.notifier, admin_client=admin_client)
    async with builder as topic_builder:
        logger.info(f"Creating topics: {builder._config.kafka_topics.values()}")  # noqa: G004, SLF001
        await topic_builder.create_all_topics()


if __name__ == "__main__":
    config = load_config()
    asyncio.run(init_notifier_topics(config=config))
