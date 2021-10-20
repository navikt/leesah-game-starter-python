from consumer import Consumer
from producer import Producer
from utils import deserialize
from schemas import Question, Answer, Ping, Pong, Registration

from schema import SchemaError
import json
from datetime import datetime

###########

TEAM_NAVN = "Team ABC"

# ##########

if __name__ == "__main__":
    consumer = Consumer()
    producer = Producer()
    producer.ping()
    for kafka_msg in consumer.consume():
        try:
            message = deserialize(kafka_msg.value)
            if Ping.is_valid(message):
                print("Received PING", datetime.now())
                producer.pong()
            elif Pong.is_valid(message):
                print("Received PONG", datetime.now())
            elif Registration.is_valid(message):
                print(f"Team {message['team_id']} har blitt registrert")
            elif Question.is_valid(message):
                svar = {
                    "msg_type": "answer",
                    "team_id": TEAM_NAVN,
                    "answer": "Dette er svaret på spørsmålet",
                }
                producer.send(svar)
                print("Svarte med:", svar)
            elif Answer.is_valid(message):
                print(f"Mottok svar fra {message['team_id']}: {message['answer']}")
            else:
                raise (SchemaError(f"Meldingsformatet på {message} er ukjent"))
        except SchemaError as e:
            print(e)
        except (json.JSONDecodeError):
            print("Fikk ikke til å parse JSON for følgende melding:", kafka_msg.value)
