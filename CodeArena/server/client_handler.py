
import json
import threading

class ClientHandler(threading.Thread):
    def __init__(self, socket, addr, queue, contest):
        super().__init__(daemon=True)
        self.socket = socket
        self.addr = addr
        self.queue = queue
        self.contest = contest

    def run(self):
        try:
            raw = self.socket.recv(50000).decode().strip()
            if not raw:
                return

            data = json.loads(raw)

            if data["type"] == "submit":

                if not self.contest.contest_active():
                    self.socket.send(b"Contest finished\n")
                    return
                task = {
                    "username": data["username"],
                    "problem_id": data["problem_id"],
                    "language": data["language"],
                    "code": data["code"],
                }
                self.queue.push((task, self.socket))
                self.socket.send(b"Submission received\n")
                return

        except Exception:
            return
