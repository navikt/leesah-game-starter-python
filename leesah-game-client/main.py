from kafka import KafkaConsumer, KafkaProducer
from schema import Schema, Or, Use, SchemaError
import json

TEAM_ID = "leesah-team-1"
QUIZ_TOPIC = "quiz-rapid"
UTF_8 = "utf-8"

Message = Schema({"msg_type": Or("question", "answer")})
Question = Schema({"msg_type": "question"})
Answer = Schema({"msg_type": "answer"})


def parse_kafka_message_to_json(msg: bytes) -> dict:
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
            message = Message.validate(parse_kafka_message_to_json(msg))
            if Question.is_valid(message):
                # svar = {"msg_type": "answer", "team": TEAM_ID, "answer": "1+1=2"}
                svar = {"msg_type": "answer"}
                print("SVARER MED:", svar)
                producer.send(QUIZ_TOPIC, bytes(json.dumps(svar), UTF_8))
            elif Answer.is_valid(message):
                print("MOTTOK SVAR:", message)
            else:
                print("Fikk inn melding som verken var spørsmål eller svar", message)
        except json.JSONDecodeError:
            print("Unable to parse JSON:", msg.value)
        except SchemaError as e:
            print("JSON følger ikke skjemaet", msg.value, e)
