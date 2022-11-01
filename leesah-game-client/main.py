import sys

from client_lib import quiz_rapid
from client_lib.config import LOCAL_KAFKA

# LEESAH QUIZ GAME CLIENT

# 1. Change TEAM_NAME variable to your team name
# 2. make sure you have downloaded and unpacked the ca.pem, service.cert and service.key in the certs/ dir

# Config ##########

TEAM_NAME = "CHANGE ME"
QUIZ_TOPIC = "quiz-rapid"
CONSUMER_GROUP_ID = f"cg-leesah-team-${TEAM_NAME}-1"
assert TEAM_NAME is not None and TEAM_NAME != "CHANGE ME", "Husk å gi teamet ditt et navn"


# #################


class MyParticipant(quiz_rapid.QuizParticipant):
    def __init__(self):
        super().__init__(TEAM_NAME)

    def handle_question(self, question: quiz_rapid.Question):
        if question.category == "team-registration":
            self.handle_register_team(question)

    def handle_assessment(self, assessment: quiz_rapid.Assessment):
        pass

    # --------------------------------------------------------------------- Question handlers

    def handle_register_team(self, question: quiz_rapid.Question):
        self.publish_answer(
            question_id=question.messageId,
            category=question.category,
            answer=TEAM_NAME
        )


def main():
    rapid = quiz_rapid.QuizRapid(
        team_name=TEAM_NAME,
        topic=QUIZ_TOPIC,
        bootstrap_servers=LOCAL_KAFKA,
        consumer_group_id=CONSUMER_GROUP_ID,
        auto_commit=False,
        logg_questions=True,
        logg_answers=False,
        short_log_line=False,
        log_ignore_list=[]
    )
    participant = MyParticipant()
    run(participant, rapid)


def run(participant, rapid):
    print("\n\t✅ Started client successfully\n")
    try:
        while rapid.running:
            rapid.run(participant)
    except KeyboardInterrupt:
        shutdown(rapid)


def shutdown(rapid):
    print("\n 🛑 shutting down...")
    rapid.close()
    sys.exit(1)
