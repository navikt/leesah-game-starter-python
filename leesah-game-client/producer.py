from typing import Dict
from config import BOOTSTRAP_SERVERS, QUIZ_TOPIC
from kafka import KafkaProducer
from utils import serialize


class Producer:
    def __init__(self) -> None:
        self.producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP_SERVERS,
            # security_protocol="SSL",
            # ssl_check_hostname=True,
            # ssl_cafile="certs/integration-test-cluster-CA.pem",
            # ssl_certfile="certs/service.cert",
            # ssl_keyfile="certs/service.key",
        )

    def send(self, msg: Dict, topic=QUIZ_TOPIC):
        self.producer.send(topic, serialize(msg))

    def ping(self):
        self.send(
            {
                "msg_type": "ping",
            }
        )

    def pong(self):
        self.send(
            {
                "msg_type": "pong",
            }
        )
