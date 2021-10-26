from client_lib import quiz_rapid
from client_lib.config import HOSTED_KAFKA, LOCAL_KAFKA
import pprint

# LEESAH QUIZ GAME CLIENT

# 1. Change TEAM_NAME variable to your team name
# 2. make sure you have downloaded and unpacked the ca.pem, service.cert and service.key in the certs/ dir

# Config ##########

TEAM_NAME = "CHANGE ME"
QUIZ_TOPIC = "quiz-rapid"
CONSUMER_GROUP_ID = f"cg-leesah-team-${TEAM_NAME}-1"

# #################


class MyParticipant(quiz_rapid.QuizParticipant):

    def __init__(self):
        super().__init__(TEAM_NAME)

    def handle_question(self, question: quiz_rapid.Question):
        pprint.pp(question)
    #    if question.category == "team-registration":
    #        self.handle_register_team(question)

    def handle_assessment(self, msg):
        pprint.pp(msg)

# --------------------------------------------------------------------- Question handlers

    def handle_register_team(self, question):
        pass
        # self.publish_answer(question.messageId, question.category, TEAM_NAME)


def main():
    rapid = quiz_rapid.QuizRapid(TEAM_NAME, QUIZ_TOPIC, HOSTED_KAFKA, CONSUMER_GROUP_ID, False)

    try:
        while True:
            rapid.run(MyParticipant())
    except KeyboardInterrupt:
        print("\nstopping...")
