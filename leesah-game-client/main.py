from client_lib import quiz_rapid
from client_lib.config import HOSTED_KAFKA, LOCAL_KAFKA
import pprint
import json

# LEESAH QUIZ GAME CLIENT

# 1. Change TEAM_NAME variable to your team name
# 2. make sure you have downloaded and unpacked the ca.pem, service.cert and service.key in the certs/ dir

# Config ##########

TEAM_NAME = "team 1"
QUIZ_TOPIC = "quiz-rapid"
CONSUMER_GROUP_ID = f"cg-leesah-team-${TEAM_NAME}-1"

# #################


class MyParticipant(quiz_rapid.QuizParticipant):
    def __init__(self):
        super().__init__(TEAM_NAME)

    def handle_question(self, question: quiz_rapid.Question):
        pprint.pp(question)

        if question.category == "team-registration":
            self.handle_register_team(question)

    def handle_assessment(self, assessment: quiz_rapid.Assessment):
        pprint.pp(assessment)

    # --------------------------------------------------------------------- Question handlers

    def handle_register_team(self, question: quiz_rapid.Question):
        print(json.dumps(question.__dict__))
        self.publish_answer(
            question_id=question.messageId,
            category=question.category,
            answer=TEAM_NAME
        )


def main():
    assert TEAM_NAME is not None and TEAM_NAME != "CHANGE ME", "Husk å gi teamet ditt et navn"
    rapid = quiz_rapid.QuizRapid(
        TEAM_NAME, QUIZ_TOPIC, LOCAL_KAFKA, CONSUMER_GROUP_ID, False
    )

    try:
        print("\n\t✅ Started client successfully\n")
        while True:
            rapid.run(MyParticipant())
    except KeyboardInterrupt:
        print("\nstopping...")
