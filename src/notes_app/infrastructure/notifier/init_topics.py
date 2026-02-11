import asyncio

from notes_app.infrastructure.config import load_config
from notes_app.infrastructure.notifier.main import create_kafka_admin_client
from notes_app.infrastructure.notifier.topic_manager import NotifierTopicManager


async def init_notifier_topics() -> None:
    config = load_config()
    notifier_topic_manager = NotifierTopicManager(
        notifier_config=config.notifier, admin_client=create_kafka_admin_client(config.notifier)
    )
    async with notifier_topic_manager as tm:
        await tm.create_all_topics()


if __name__ == "__main__":
    asyncio.run(init_notifier_topics())
