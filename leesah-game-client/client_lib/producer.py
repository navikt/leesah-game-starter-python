import json
from typing import Dict

from kafka import KafkaProducer

from .config import CA_PATH, CERT_PATH, KEY_PATH, ENCODING


class Producer:
    def __init__(self, topic: str, bootstrap_servers: str) -> None:
        self._topic = topic
        if "localhost" in bootstrap_servers:
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
            )
        else:
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                security_protocol="SSL",
                ssl_check_hostname=True,
                ssl_cafile=CA_PATH,
                ssl_certfile=CERT_PATH,
                ssl_keyfile=KEY_PATH,
            )

    def send(self, msg: Dict, topic=None):
        if topic is None:
            topic = self._topic
        self.producer.send(topic, serialize(msg))


serialize = lambda value: json.dumps(value).encode(ENCODING)