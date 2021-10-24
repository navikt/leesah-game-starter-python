from pathlib import Path

HOSTED_KAFKA = "nav-integration-test-kafka-nav-integration-test.aivencloud.com:26484"
LOCAL_KAFKA = "localhost:29092"
CONSUMER_GROUP_ID = "leesah-game-consumer-5"
QUIZ_TOPIC = "quiz-rapid"
ENCODING = "utf-8"

CA_PATH = Path("certs/ca.pem")
CERT_PATH = Path("certs/service.cert")
KEY_PATH = Path("certs/service.key")

assert CA_PATH.is_file()
assert CERT_PATH.is_file()
assert KEY_PATH.is_file()
