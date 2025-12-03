import json
import os
import random
from server.settings import PROBLEMS_DIR

class ContestFactory:
    def __init__(self):
        pass

    def load_problem(self, problem_id):
        base = os.path.join(PROBLEMS_DIR, problem_id)
        with open(os.path.join(base, "meta.json")) as f:
            meta = json.load(f)
        return meta

    def generate_contest(self, num_problems, difficulty):
        all_problems = [
            d for d in os.listdir(PROBLEMS_DIR)
            if os.path.isdir(os.path.join(PROBLEMS_DIR, d))
        ]

        # filtrer par difficulté
        filtered = []
        for p in all_problems:
            meta_path = os.path.join(PROBLEMS_DIR, p, "meta.json")
            with open(meta_path) as f:
                meta = json.load(f)
                if meta["difficulty"] == difficulty:
                    filtered.append(p)

        if len(filtered) < num_problems:
            raise ValueError("Pas assez de problèmes pour cette difficulté.")

        return random.sample(filtered, num_problems)
