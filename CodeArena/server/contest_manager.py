import time
import threading
from server.contest_factory import ContestFactory
from server.settings import DEFAULT_CONTEST_DURATION

class ContestManager:
    def __init__(self):
        self.active_contest = None
        self.remaining_time = 0
        self.lock = threading.Lock()

    def create_contest(self, num_problems, difficulty):
        factory = ContestFactory()
        problems = factory.generate_contest(num_problems, difficulty)

        with self.lock:
            self.active_contest = {
                "problems": problems,
                "difficulty": difficulty,
                "duration": DEFAULT_CONTEST_DURATION,
            }
            self.remaining_time = DEFAULT_CONTEST_DURATION

        threading.Thread(target=self._timer_thread, daemon=True).start()
        return self.active_contest

    def _timer_thread(self):
        while self.remaining_time > 0:
            time.sleep(1)
            with self.lock:
                self.remaining_time -= 1

    def get_remaining_time(self):
        with self.lock:
            return self.remaining_time

    def contest_active(self):
        return self.remaining_time > 0
