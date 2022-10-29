import dataclasses
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
import enum
from typing import Set

from confluent_kafka import Consumer, Producer
from .kafka import consumer_config, producer_config

from .schemas import (Question as SchemaQuestion, Assessment as SchemaAssessment)
from .config import ENCODING


deserialize = lambda value: json.loads(value.decode(ENCODING))
serialize = lambda value: json.dumps(value).encode(ENCODING)

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
        """
        handle questions received from the quiz topic.

        Parameters
        ----------
            question : Question
                question issued by the quizmaster

        """
        pass

    @abstractmethod
    def handle_assessment(self, assessment: Assessment):
        """
        handle assessments received from the quiz topic.

        Parameters
        ----------
            assessment : Assessment
                assessment of an answer by the quizmaster

        """
        pass

    def publish_answer(self, question_id: str, category: str, answer: str):
        """
        publishes an answer to a specific question id with a category

        Parameters
        ----------
            question_id : str
                the messageId of the question to be answered
            category : str
                the category of the question to be answered
            answer : str
                the answer to the question asked

        """
        self.publish(Answer(question_id, category, self._team_name, answer))

    def publish(self, answer: Answer):
        self._outbox.add(answer)

    def messages(self) -> Set[Answer]:
        out = self._outbox
        self._outbox = set()
        return out


class QuizRapid:
    """Mediates messages to and from the quiz rapid on behalf of the quiz participant"""

    def __init__(self,
                 team_name: str,
                 topic: str,
                 bootstrap_servers: str,
                 consumer_group_id: str,
                 auto_commit: bool = True,
                 producer=None,
                 consumer=None):
        """
        Constructs all the necessary attributes for the QuizRapid object.

        Parameters
        ----------
            team_name : str
                team name to filter messages on
            topic : str
                topic to produce and consume messages
            bootstrap_servers : str
                kafka host server
            consumer_group_id : str
                the kafka consumer group id to commit offset on
            auto_commit : bool, optional
                auto commit offset for the consumer (default is True)
            producer : Producer, optional
                specify a custom Producer to use (Default None)
            consumer : Consumer, optional
                specify a custom consumer to use (Default None)
        """
        if consumer is None:
            consumer = Consumer(consumer_config(bootstrap_servers, consumer_group_id, auto_commit))
            consumer.subscribe([topic])
        if producer is None:
            producer = Producer(producer_config(bootstrap_servers))
        self._name = team_name
        self._producer = producer
        self._consumer = consumer
        self._topic = topic
        self._commit_offset = auto_commit

    def run(self, participant: QuizParticipant):
        msg = self._consumer.poll(timeout=1000)
        if msg is None:
            return
        msg = deserialize(msg.value())
        if SchemaQuestion.is_valid(msg):
            participant.handle_question(
                Question(msg["messageId"], msg["question"], msg["category"], msg["type"]))
        if SchemaAssessment.is_valid(msg) and msg["teamName"] == self._name:
            participant.handle_assessment(
                Assessment(msg["messageId"], msg["category"], msg["teamName"], msg["questionId"],
                           msg["answerId"], AssessmentStatus[msg["status"].upper()], msg["sign"], msg["type"]))
        for message in participant.messages():
            self._producer.produce(topic=self._topic, value=serialize(dataclasses.asdict(message)))

        if self._commit_offset:
            self.commit_offset()

    def commit_offset(self):
        self._consumer.consumer.commit()

