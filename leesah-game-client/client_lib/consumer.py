from kafka import KafkaConsumer

from .config import (
    CONSUMER_GROUP_ID,
    QUIZ_TOPIC,
    HOSTED_KAFKA,
    LOCAL_KAFKA,
)


class Consumer:
    def __init__(self, auto_commit: bool, local_kafka=True) -> None:
        self.topic = QUIZ_TOPIC
        if local_kafka:
            self.consumer = KafkaConsumer(
                bootstrap_servers=LOCAL_KAFKA,
                group_id=CONSUMER_GROUP_ID,
                auto_offset_reset="earliest",
            )
        else:
            self.consumer = KafkaConsumer(
                bootstrap_servers=HOSTED_KAFKA,
                group_id=CONSUMER_GROUP_ID,
                auto_offset_reset="earliest",
                security_protocol="SSL",
                ssl_check_hostname=True,
                ssl_cafile="certs/ca.pem",
                ssl_certfile="certs/service.cert",
                ssl_keyfile="certs/service.key",
                enable_auto_commit=auto_commit
            )
        self.consumer.subscribe(QUIZ_TOPIC)


