from schema import Schema

Question = Schema({"msg_type": "question"})
Answer = Schema({"msg_type": "answer", "team_id": str, "answer": str})
Registration = Schema({"msg_type": "registration", "team_id": str})
Ping = Schema({"msg_type": "ping"})
Pong = Schema({"msg_type": "pong"})
