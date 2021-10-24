import dataclasses
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
import enum

from .producer import Producer
from .consumer import Consumer
from .schemas import (Question as SchemaQuestion, Assessment as SchemaAssessment)
from . import config


@dataclass(eq=True, frozen=True)
class Answer:
    questionId: str
    category: str
    teamName: str
    answer: str
    messageId: str = str(uuid.uuid4())
    type: str = "ANSWER"


@dataclass
class Question:
    messageId: str
    question: str
    category: str
    type: str = "QUESTION"


class AssessmentStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

@dataclass
class Assessment:
    messageId: str
    category: str
    teamName: str
    questionId: str
    answerId: str
    status: AssessmentStatus
    sign: str
    type: str = "ASSESSMENT"


class QuizParticipant(ABC):

    def __init__(self, team_name: str):
        self._outbox = set()
        self._team_name = team_name

    @abstractmethod
    def handle_question(self, question: Question):
        pass

    @abstractmethod
    def handle_assessment(self, assessment: Assessment):
        pass

    def publish_answer(self, question_id: str, category: str, answer: str):
        self.publish(Answer(question_id, category, self._team_name, answer))

    def publish(self, answer: Answer):
        self._outbox.add(answer)

    def messages(self) -> set[Answer]:
        out = self._outbox
        self._outbox = set()
        return out


class QuizRapid:

    def __init__(self,
                 team_name: str,
                 topic: str,
                 auto_commit: bool = True,
                 producer=Producer(local_kafka=False),
                 consumer=None):
        if consumer is None:
            consumer = Consumer(auto_commit=auto_commit, local_kafka=False)
        self._name = team_name
        self._producer = producer
        self._consumer = consumer
        self._topic = topic
        self._commit_offset = auto_commit

    def run(self, participant: QuizParticipant):
        raw_msgs = self._consumer.consumer.poll(timeout_ms=1000)
        for tp, msgs in raw_msgs.items():
            for msg in msgs:
                msg = deserialize(msg.value)
                if SchemaQuestion.is_valid(msg):
                    participant.handle_question(Question(msg["messageId"], msg["question"], msg["category"], msg["type"]))
                if SchemaAssessment.is_valid(msg) and msg["teamName"] == self._name:
                    participant.handle_assessment(Assessment(msg["messageId"], msg["category"], msg["teamName"], msg["questionId"], msg["answerId"], AssessmentStatus[msg["status"].upper()], msg["sign"], msg["type"]))
        for message in participant.messages():
            self._producer.send(dataclasses.asdict(message), self._topic)

        if self._commit_offset:
            self._consumer.consumer.commit()



deserialize = lambda value: json.loads(value.decode(config.ENCODING))
