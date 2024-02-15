# LEESAH Python

> Leesah-game er et hendelsedrevet applikasjonsutviklingspill som utfordrer spillerne til å bygge en hendelsedrevet applikasjon. 
> Applikasjonen håndterer forskjellige typer oppgaver som den mottar som hendelser på en Kafka-basert hendelsestrøm. 
> Oppgavene varierer fra veldig enkle til mer komplekse.

Python-bibliotek for å spille LEESAH!

## Kom i gang

Det finnes to versjoner av Leesah-game!
En hvor man lager en applikasjon som kjører på Nais, og en hvor man spiller lokalt direkte fra terminalen sin.
Dette biblioteket kan brukes i begge versjoner, men denne dokumentasjonen dekker kun lokal spilling.
Vi har et eget template-repo som ligger under [navikt/leesah-game-template-go](https://github.com/navikt/leesah-game-template-go) for å spille Nais-versjonen.

### Hent credentials

Sertifikater for å koble seg på Kafka ligger tilgjengelig på [leesah-game-cert.ekstern.dev.nav.no/certs](https://leesah-game-cert.ekstern.dev.nav.no/certs), brukernavn og passord skal du få utdelt.
Du kan også bruke kommandoen nedenfor:

```bash
wget --user <username> --password <password> -O leesah-creds.zip https://leesah-game-cert.ekstern.dev.nav.no/certs && unzip leesah-creds.zip 
```

### Eksempelkode

Nedenfor er det et fungerende eksempel som svarer på lagregistreringsspørsmålet med et navn du velger, og en farge du velger:

```python
import leesah

TEAM_NAME = "CHANGE ME"
HEX_CODE = "CHANGE ME"


def handle_questions(question: leesah.Question):
    """Call when a question is received from the stream.

    The return value is your answer to the question.
    """
    print(f"Received question: {question}")
    if question.category == "team-registration":
        return HEX_CODE


def main():
    """Run the quiz client."""
    rapid = leesah.QuizRapid(TEAM_NAME)
    rapid.run(handle_questions)
```

## Kjør lokalt

Vi anbefaler at du bruker et virtuelt miljø for å kjøre koden din, som for eksempel [Venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/).

**For macOS/Linux**
```shell
cd leesah-game-starter
python3 -m venv venv
source ./venv/bin/activate
```

**For Windows**
```shell
cd leesah-game-starter
python3 -m venv venv
.\venv\Scripts\activate
```

Er kun en avhengighet du trenger, og det er [leesah](https://pypi.org/project/leesah/).

```shell
python3 -m pip install leesah
```

Kjør koden din med:

```shell
python3 main.py
```
