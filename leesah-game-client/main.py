from kafka import KafkaConsumer, KafkaProducer
import json

TEAM_ID = "leesah-team-1"
QUIZ_TOPIC = "quiz-rapid"
UTF_8 = "utf-8"


def parse_kafka_message(msg: bytes) -> dict:
    return json.loads(msg.value.decode(UTF_8))


if __name__ == "__main__":
    consumer = KafkaConsumer(
        QUIZ_TOPIC,
        bootstrap_servers="localhost:29092",
        group_id=TEAM_ID,
        auto_offset_reset="earliest",
    )
    producer = KafkaProducer(bootstrap_servers="localhost:29092")
    for msg in consumer:
        try:
            parsed_msg = parse_kafka_message(msg)
            # TODO: use proper schema matching when parsing JSON
            if parsed_msg["type"] == "question":
                svar = {"type": "svar", "innhold": "1+1=2"}
                print("SVARER MED:", svar)
                producer.send(QUIZ_TOPIC, bytes(json.dumps(svar), UTF_8))
            elif parsed_msg["type"] == "svar":
                print("MOTTOK SVAR:", parsed_msg)
            else:
                print("Fikk inn melding som verken var spørsmål eller svar", parsed_msg)
        except json.JSONDecodeError:
            print("Unable to parse JSON:", msg.value)
        except KeyError as e:
            print("JSON følger ikke skjemaet", msg.value, e)
