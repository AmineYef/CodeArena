import threading
from workers.worker_pool import WorkerPool

class Dispatcher:
    def __init__(self, queue, leaderboard, contest):
        self.queue = queue
        self.leaderboard = leaderboard
        self.contest = contest
        self.pool = WorkerPool()
        self.thread = threading.Thread(target=self._loop, daemon=True)

    def start(self):
        self.thread.start()

    def _loop(self):
        while True:
            item = self.queue.pop()
            if item is None:
                continue

            # 🔥 item = (task, socket)
            task, client_socket = item

            result = self.pool.execute(task)

            # leaderboard
            self.leaderboard.update(task["username"], result["verdict"])

            # 🔥 ENVOI DU VERDICT
            client_socket.send((result["verdict"] + "\n").encode())

