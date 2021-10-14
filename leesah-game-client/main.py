from kafka import KafkaConsumer, KafkaProducer
from schema import Schema, SchemaError
import json

HOST = "localhost:29092"
CONSUMER_GROUP_ID = "leesah-game-consumer-1"
QUIZ_TOPIC = "quiz-rapid"
UTF_8 = "utf-8"

Question = Schema({"msg_type": "question"})
Answer = Schema({"msg_type": "answer", "team_id": str, "answer": str})
Registration = Schema({"msg_type": "registration", "team_id": str})

serialize = lambda value: json.dumps(value).encode(UTF_8)
deserialize = lambda value: json.loads(value.decode(UTF_8))

###########

TEAM_NAVN = "Team ABC"

###########

if __name__ == "__main__":
    consumer = KafkaConsumer(
        bootstrap_servers=HOST,
        group_id=CONSUMER_GROUP_ID,
        auto_offset_reset="earliest",
    )
    producer = KafkaProducer(
        bootstrap_servers=HOST,
    )
    consumer.subscribe(QUIZ_TOPIC)
    for kafka_msg in consumer:
        try:
            message = deserialize(kafka_msg.value)
            if Registration.is_valid(message):
                print(f"Team {message['team_id']} har blitt registrert")
            elif Question.is_valid(message):
                svar = {
                    "msg_type": "answer",
                    "team_id": TEAM_NAVN,
                    "answer": "Dette er svaret på spørsmålet",
                }
                producer.send(QUIZ_TOPIC, serialize(svar))
                print("Svarte med:", svar)
            elif Answer.is_valid(message):
                print(f"Mottok svar fra {message['team_id']}: {message['answer']}")
            else:
                raise (SchemaError(f"Meldingsformatet på {message} er ukjent"))
        except SchemaError as e:
            print(e)
        except (json.JSONDecodeError):
            print("Fikk ikke til å parse JSON for følgende melding:", kafka_msg.value)
