from collections import Iterator
from kafka import KafkaConsumer
from config import (
    CONSUMER_GROUP_ID,
    QUIZ_TOPIC,
    BOOTSTRAP_SERVERS,
)


class Consumer:
    def __init__(self) -> None:
        self.topic = QUIZ_TOPIC
        self.consumer = KafkaConsumer(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            group_id=CONSUMER_GROUP_ID,
            auto_offset_reset="earliest",
            # security_protocol="SSL",
            # ssl_check_hostname=True,
            # ssl_cafile="certs/integration-test-cluster-CA.pem",
            # ssl_certfile="certs/service.cert",
            # ssl_keyfile="certs/service.key",
        )
        self.consumer.subscribe(QUIZ_TOPIC)

    def consume(self) -> Iterator:
        # TODO: use this function as a deserializing middleware
        return self.consumer
