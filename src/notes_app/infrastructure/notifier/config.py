from dataclasses import dataclass


@dataclass(frozen=True)
class NotifierConfig:
    bootstrap_servers: str

    # producer_settings
    request_timeout_ms: int = 30000
    retry_backoff_ms: int = 1000
    connections_max_idle_ms: int = 600000

    # note_created_topic
    note_created_topic_name: str = "note-created"
    note_created_topic_num_partitions: int = 1
    note_created_topic_replication_factor: int = 1

    # note_deleted_topic
    note_deleted_topic_name: str = "note-deleted"
    note_deleted_topic_num_partitions: int = 1
    note_deleted_topic_replication_factor: int = 1
