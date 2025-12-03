import threading
from server.settings import (
    POINTS_CORRECT, POINTS_WRONG_ANSWER, POINTS_TIMEOUT,
    POINTS_COMPILATION_ERROR, POINTS_RUNTIME_ERROR
)

class Leaderboard:
    def __init__(self):
        self.scores = {}   # { username : {score, solved, penalty} }
        self.lock = threading.Lock()

    def update(self, username, verdict):
        with self.lock:
            if username not in self.scores:
                self.scores[username] = {
                    "score": 0,
                    "solved": 0,
                    "penalty": 0
                }

            if verdict == "OK":
                self.scores[username]["score"] += POINTS_CORRECT
                self.scores[username]["solved"] += 1

            elif verdict == "WRONG_ANSWER":
                self.scores[username]["score"] += POINTS_WRONG_ANSWER

            elif verdict == "TIMEOUT":
                self.scores[username]["score"] += POINTS_TIMEOUT

            elif verdict == "COMPILATION_ERROR":
                self.scores[username]["score"] += POINTS_COMPILATION_ERROR

            elif verdict == "RUNTIME_ERROR":
                self.scores[username]["score"] += POINTS_RUNTIME_ERROR

    def get_leaderboard(self):
        with self.lock:
            result = []
            for user, data in self.scores.items():
                result.append({
                    "user": user,
                    "score": data["score"],
                    "solved": data["solved"],
                    "penalty": data["penalty"]
                })
            return sorted(result, key=lambda x: (-x["score"], -x["solved"]))
