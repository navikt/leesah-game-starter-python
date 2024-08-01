import dataclasses
import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from json import JSONDecodeError
from typing import Set

from confluent_kafka import Consumer, Producer
from .kafka import consumer_config, producer_config

ANSWER_LOG_COLOR = "\u001b[34m"
QUESTION_LOG_COLOR = "\u001b[32m"

deserialize = lambda value: json.loads(value.decode())
serialize = lambda value: json.dumps(value, ensure_ascii=False).encode()

@dataclass(eq=True, frozen=True)
class Svar:
    kategorinavn: str
    lagnavn: str
    svar: str
    spørsmålId: str
    svarId: str = str(uuid.uuid4())
    opprettet: str = datetime.now().isoformat()

@dataclass
class Spørsmål:
    spørsmålId: str
    spørsmål: str
    kategorinavn: str
    svarFormat: str
    type: str = "SPØRSMÅL"


class QuizParticipant(ABC):

    def __init__(self, lagnavn: str):
        self._outbox = set()
        self._lagnavn = lagnavn

    @abstractmethod
    def håndter_spørsmål(self, spørsmål: Spørsmål):
        """
        handle questions received from the quiz topic.

        Parameters
        ----------
            question : Question
                question issued by the quizmaster

        """
        pass

    def publiser_svar(self, spørsmål_id: str, kategorinavn: str, svar: str):
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
        self.publish(Svar(spørsmålId=spørsmål_id, kategorinavn=kategorinavn, lagnavn=self._lagnavn, svar=svar))

    def publish(self, svar: Svar):
        self._outbox.add(svar)

    def messages(self) -> Set[Svar]:
        out = self._outbox
        self._outbox = set()
        return out


class QuizRapid:
    """Mediates messages to and from the quiz rapid on behalf of the quiz participant"""

    def __init__(self,
                 lagnavn: str,
                 topic: str,
                 bootstrap_servers: str,
                 consumer_group_id: str,
                 auto_commit: bool = True,
                 producer=None,
                 consumer=None,
                 logg_questions=False,
                 logg_answers=False,
                 short_log_line=False,
                 log_ignore_list=None):
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
            logg_questions : bool, optional
                should the QuizRapid logg incoming questions to the terminal (Default False)
            logg_answers : bool, optional
                should the QuizRapid logg outgoing answers to the terminal (Default False)
            short_log_line : bool, optional
                for enabled loggers, should the output be shortened keeping only essential fields (Default False)
            log_ignore_list : list, optional
                for enabled loggers, should any question categories be ignored (Default None)
        """
        self.running = True
        if consumer is None:
            consumer = Consumer(consumer_config(bootstrap_servers, consumer_group_id, auto_commit))
            consumer.subscribe([topic])
        if producer is None:
            producer = Producer(producer_config(bootstrap_servers))
        self._name = lagnavn
        self._producer: Producer = producer
        self._consumer: Consumer = consumer
        self._topic = topic
        self._commit_offset = auto_commit
        self._logg_questions = logg_questions
        self._logg_answers = logg_answers
        self._short_log_line = short_log_line
        self._log_ignore_list = log_ignore_list

    def run(self, participant: QuizParticipant):
        msg = self._consumer.poll(timeout=1)
        if msg is None:
            return
        try:
            msg = deserialize(msg.value())
        except JSONDecodeError as e:
            print(f"error: could not parse message: {msg.value()} error: {e}")
            return
        if "@event_name" in msg and msg["@event_name"] == "SPØRSMÅL" and "spørsmål" in msg:
            spørsmål = Spørsmål(spørsmålId=msg["spørsmålId"], spørsmål=msg["spørsmål"], kategorinavn=msg["kategorinavn"], svarFormat="")
            self._logg_spørsmål(spørsmål)
            participant.håndter_spørsmål(spørsmål)
        for message in participant.messages():
            self._logg_spørsmål(message)
            data = dataclasses.asdict(message)
            data.pop('opprettet')
            data['@event_name'] = "SVAR"
            data['@opprettet'] = datetime.now().isoformat()
            value = serialize(data)
            self._producer.produce(topic=self._topic, value=value)
            self._producer.flush(timeout=0.1)
        if self._commit_offset:
            self.commit_offset()

    def commit_offset(self):
        self._consumer.commit()

    def close(self):
        self.running = False
        self._producer.flush()
        self._consumer.close()

    def _logg_spørsmål(self, spørsmål: Spørsmål):
        if self._logg_questions and (self._log_ignore_list is None or spørsmål.kategorinavn not in self._log_ignore_list):
            question_dict = dataclasses.asdict(spørsmål)
            if self._short_log_line:
                question_dict.pop("spørsmålId")
                question_dict.pop("type")
            print("\x1b[33;20m [{}][Q]\x1b[0m {}{}\x1b[0m"
                  .format(datetime.now().time().isoformat(), QUESTION_LOG_COLOR, json.dumps(question_dict, ensure_ascii=False), ))

    def _logg_svar(self, svar: Svar):
        if self._logg_answers and (self._log_ignore_list is None or svar.kategorinavn not in self._log_ignore_list):
            answer_dict = dataclasses.asdict(svar)
            if self._short_log_line:
                answer_dict.pop("svarId")
                answer_dict.pop("type")
                answer_dict.pop("spørsmålId")
                answer_dict.pop("lagnavn")
            print("\x1b[33;20m [{}][A]\x1b[0m {}{}\x1b[0m"
                  .format(datetime.now().time().isoformat(), ANSWER_LOG_COLOR, json.dumps(answer_dict, ensure_ascii=False)))
