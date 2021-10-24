from client_lib import quiz_rapid
import pprint

###########

TEAM_NAVN = "cool-team"


# ##########


class MyParticipant(quiz_rapid.QuizParticipant):

    def __init__(self):
        super().__init__(TEAM_NAVN)

    def handle_question(self, question: quiz_rapid.Question):
        print("received question")
        pprint.pp(question)
        if question.category == "team-registration":
            self.handle_register_team(question)

    def handle_assessment(self, msg):
        print("received assessment")
        pprint.pp(msg)

    # --------------------------------------------------------------------- Question handlers

    def handle_register_team(self, question):
        pass
        # self.publish_answer(question.messageId, question.category, TEAM_NAVN)


def main():
    rapid = quiz_rapid.QuizRapid(TEAM_NAVN, "quiz-rapid", False)
    while True:
        rapid.run(MyParticipant())


if __name__ == "__main__":
    main()
