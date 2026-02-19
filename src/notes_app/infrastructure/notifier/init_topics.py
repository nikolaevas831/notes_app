import asyncio
from logging import getLogger

from notes_app.infrastructure.config import load_config
from notes_app.infrastructure.logging.main import setup_logging
from notes_app.infrastructure.notifier.config import NotifierConfig
from notes_app.infrastructure.notifier.main import create_kafka_admin_client
from notes_app.infrastructure.notifier.topic_manager import NotifierTopicBuilder

logger = getLogger(__name__)


async def init_notifier_topics(config: NotifierConfig) -> None:
    notifier_topic_builder = NotifierTopicBuilder(
        notifier_config=config, admin_client=create_kafka_admin_client(config)
    )
    async with notifier_topic_builder as tm:
        logger.info(f"Creating topics: {config.kafka_topics.values()}")  # noqa: G004
        await tm.create_all_topics()


if __name__ == "__main__":
    config = load_config()
    setup_logging(config=config.logging)
    asyncio.run(init_notifier_topics(config=config.notifier))
