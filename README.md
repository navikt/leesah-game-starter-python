# LEESAH Quiz Client

**System overview**
```bash
┌──────────────┐       ┌──────────────┐
│              │       │              │
│              │       │              │
│  Quizboard   │       │  Quizmaster  │
│              │       │              │
│              │       │              │
└──────────────┘       └──────────────┘
│  ▲                   │  ▲
│  │                   │  │
│  │                   │  │
▼  │                   ▼  │
┌──────────────────────────────────────────────────────────────┐
│                      Kafka                                   │
└──────────────────────────────────────────────────────────────┘
▲    │                           ▲    │
│    │                           │    │
│    ▼                           │    ▼
┌──────────────┐                 ┌──────────────┐
│              │                 │              │
│              │                 │              │
│    Team 1    │      .  .  .    │    Team n    │
│              │                 │              │
│              │                 │              │
└──────────────┘                 └──────────────┘
````
## Setup 📝

### 1.Setup virtual environment for the project

We recommend to use a virtual environment to install the dependencies. Set one up using

**For macOS/Linux**
```bash
cd leesah-game-starter
python3 -m venv venv
source ./venv/bin/activate
```

**For Windows**
```bash
cd leesah-game-starter
python3 -m venv venv
.\venv\Scripts\activate
```

or see guide [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)

### 2. Install dependencies 

```bash
python3 -m pip install -r requirements.txt
```


### 3. Run the application

Run the application from the terminal using:

```bash
python3 leesah-game-client
```
*The project comes with a \_\_main\_\_.py file that makes the directory runnable*

## Developing your quiz participant 🤖

Your challenge is to implement a QuizParticipant that answers all the question messages that are
published by the quizmaster 🧙. You are free to develop your application as you want but this starter project comes with 
som useful boilerplate so you can focus on the fun part, answering questions! 🎉

The code you need to extend is all located in `./lessah-game-client/main.py` when you run `python3 leesah-game-client` 
the `main()` function in `./lessah-game-client/main.py` is ran.

### Main loop
The main loop creates a `QuizRapid` object that runs your `QuizParticipant`. 

```python
def main():
    rapid = quiz_rapid.QuizRapid(TEAM_NAME, QUIZ_TOPIC, HOSTED_KAFKA, CONSUMER_GROUP_ID, False)

    try:
        while True:
            rapid.run(MyParticipant())
    except KeyboardInterrupt:
        print("\nstopping...")

```

### QuizParticipant
Again you are free to program the application as you like but the `QuizParticipant` is a handy abstract class you
can extend to get started solving the questions.

**Extending the QuizParticipant**
There are two methods you need to implement in your own class. 

- `handle_question(self, question: quiz_rapid.Question)` Is the most important method, it is where you will receive questions to answer.
- `handle_assessment(self, assessment: Assessment):` Allows you to read assessments the quizmaster make of your answers


## Tips and Tricks 💡

**1. Dont be afraid to answer several times to the same question** *(Except for questions that requires you don't)*

**2. Filter out question categories and write handler functions**
