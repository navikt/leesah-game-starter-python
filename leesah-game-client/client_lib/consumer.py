from kafka import KafkaConsumer

from .config import (
    CA_PATH, CERT_PATH, KEY_PATH,
)


class Consumer:
    def __init__(self, topic: str, auto_commit: bool, consumer_group_id: str, bootstrap_servers: str) -> None:
        self.topic = topic
        if "localhost" in bootstrap_servers:
            self.consumer = KafkaConsumer(
                bootstrap_servers=bootstrap_servers,
                group_id=consumer_group_id,
                auto_offset_reset="earliest",
                auto_commit=auto_commit
            )
        else:
            self.consumer = KafkaConsumer(
                bootstrap_servers=bootstrap_servers,
                group_id=consumer_group_id,
                auto_offset_reset="earliest",
                security_protocol="SSL",
                ssl_check_hostname=True,
                ssl_cafile=CA_PATH,
                ssl_certfile=CERT_PATH,
                ssl_keyfile=KEY_PATH,
                enable_auto_commit=auto_commit
            )
        self.consumer.subscribe([topic])


