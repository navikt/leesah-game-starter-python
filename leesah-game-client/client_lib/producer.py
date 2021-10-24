import json
from typing import Dict
from .config import QUIZ_TOPIC, LOCAL_KAFKA, HOSTED_KAFKA, CA_PATH, CERT_PATH, KEY_PATH, ENCODING
from kafka import KafkaProducer


class Producer:
    def __init__(self, local_kafka=True) -> None:
        if local_kafka:
            self.producer = KafkaProducer(
                bootstrap_servers=LOCAL_KAFKA,
            )
        else:
            self.producer = KafkaProducer(
                bootstrap_servers=HOSTED_KAFKA,
                security_protocol="SSL",
                ssl_check_hostname=True,
                ssl_cafile=CA_PATH,
                ssl_certfile=CERT_PATH,
                ssl_keyfile=KEY_PATH,
            )

    def send(self, msg: Dict, topic=QUIZ_TOPIC):
        self.producer.send(topic, serialize(msg))


serialize = lambda value: json.dumps(value).encode(ENCODING)