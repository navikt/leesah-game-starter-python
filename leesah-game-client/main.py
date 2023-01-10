from client_lib import quiz_rapid
from client_lib.config import HOSTED_KAFKA

# LEESAH QUIZ GAME CLIENT

# 1. Change TEAM_NAME variable to your team name
# 2. Change HEX_CODE variable to your favorite color
# 3. Change QUIZ_TOPIC variable to the quiz topic
# 4. Make sure you have downloaded and unpacked the credential files in the certs/ dir

# Config ##########################################################################################################

TEAM_NAME = "CHANGE ME"
HEX_CODE = "CHANGE ME"
QUIZ_TOPIC = "CHANGE ME"
CONSUMER_GROUP_ID = f"cg-leesah-team-${TEAM_NAME}-1"
assert TEAM_NAME is not None and TEAM_NAME != "CHANGE ME", "Husk å gi teamet ditt et navn"
assert HEX_CODE is not None and HEX_CODE != "CHANGE ME", "Husk å gi teamet ditt en farge"
assert QUIZ_TOPIC is not None and QUIZ_TOPIC != "CHANGE ME", "Husk å sett riktig topic navn"

# ##################################################################################################################


class MyParticipant(quiz_rapid.QuizParticipant):
    def __init__(self):
        super().__init__(TEAM_NAME)

    def handle_question(self, question: quiz_rapid.Question):
        raise NotImplementedError("Her må du implementere håndtering av spørsmål 😎")
        # if question.category == "team-registration":
        #     self.handle_register_team(question)

    def handle_assessment(self, assessment: quiz_rapid.Assessment):
        # Her kan du implementere feks loggig av assessments om du ønsker
        pass

# Question handlers ################################################################################################

    # def handle_register_team(self, question: quiz_rapid.Question):
    #     self.publish_answer(
    #         question_id=question.messageId,
    #         category=question.category,
    #         team_name=TEAM_NAME,
    #         answer=HEX_CODE
    #     )

#####################################################################################################################


def main():
    rapid = quiz_rapid.QuizRapid(
        team_name=TEAM_NAME,
        topic=QUIZ_TOPIC,
        bootstrap_servers=HOSTED_KAFKA,
        consumer_group_id=CONSUMER_GROUP_ID,
        auto_commit=False,     # Bare skru på denne om du vet hva du driver med :)
        logg_questions=True,   # Logg spørsmålene appen mottar
        logg_answers=True,     # Logg svarene appen sender
        short_log_line=False,  # Logg bare en forkortet versjon av meldingene
        log_ignore_list=[]     # Liste med spørsmålskategorier loggingen skal ignorere
    )
    return MyParticipant(), rapid
