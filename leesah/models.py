"""Models for the game."""

from dataclasses import dataclass
from datetime import datetime
import uuid
from pydantic import BaseModel


@dataclass(eq=True, frozen=True)
class Answer(BaseModel):
    """An answer to a question."""

    questionId: str
    category: str
    teamName: str
    answer: str
    created: str = datetime.now().isoformat()
    messageId: str = str(uuid.uuid4())
    type = "ANSWER"


@dataclass
class Question(BaseModel):
    """A question."""

    category: str
    question: str
