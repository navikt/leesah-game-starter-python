from kafka import KafkaConsumer, KafkaProducer
from random import random

TEAM_ID = "leesah-team-1"
TOPIC = "quiz-rapid"

if __name__ == "__main__":
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers="localhost:29092",
        group_id=TEAM_ID,
        auto_offset_reset="earliest",
    )
    producer = KafkaProducer(bootstrap_servers="localhost:29092")
    for msg in consumer:
        parsed_msg = msg.value.decode()
        print(parsed_msg)
        if parsed_msg == "challenge1":
            print("SVARER PÅ CHALLENGE")
            producer.send(TOPIC, b"answer to challenge1")
