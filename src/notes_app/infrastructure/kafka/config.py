from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    note_created_topic: str = "note.created"
    note_deleted_topic: str = "note.deleted"


kafka_settings = KafkaSettings()
