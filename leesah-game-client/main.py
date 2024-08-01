import uuid

from client_lib import quiz_rapid
from client_lib.config import HOSTED_KAFKA

# LEESAH QUIZ GAME CLIENT

# 1. Set `TEAM_NAME` to your preferred team name
# 2. Set `HEX_CODE` to your preferred team color
# 3. Set `QUIZ_TOPIC` to the topic name provided by the course administrators
# 4. Make sure you have downloaded and unpacked the credential files in the certs/ dir

# Config ##########################################################################################################

LAGNAVN = "<FYLL_MEG_UT>"
HEX_CODE = "<FYLL_MEG_UT>"
QUIZ_TOPIC = "<FYLL_MEG_UT>"
CONSUMER_GROUP_ID = f"cg-leesah-team-${LAGNAVN}-1"


# ##################################################################################################################


class MyParticipant(quiz_rapid.QuizParticipant):
    def __init__(self):
        super().__init__(LAGNAVN)

    def håndter_spørsmål(self, spørsmål: quiz_rapid.Spørsmål):
        if spørsmål.kategorinavn == "team-registration":
            self.håndter_team_registration(spørsmål)

    # ---------------------------------------------------------------------------- Question handlers

    def håndter_team_registration(self, spørsmål: quiz_rapid.Spørsmål):
        # Se i readm'en for å få et forslag på hvordan dette kan håndteres 🤠

def main():
    rapid = quiz_rapid.QuizRapid(
        lagnavn=LAGNAVN,
        topic=QUIZ_TOPIC,
        bootstrap_servers=HOSTED_KAFKA,
        consumer_group_id=str(uuid.uuid4()),
        auto_commit=False,  # Bare skru på denne om du vet hva du driver med :)
        logg_questions=True,  # Logg spørsmålene appen mottar
        logg_answers=True,  # Logg svarene appen sender
        short_log_line=False,  # Logg bare en forkortet versjon av meldingene
        log_ignore_list=[]  # Liste med spørsmålskategorier loggingen skal ignorere
    )
    return MyParticipant(), rapid
