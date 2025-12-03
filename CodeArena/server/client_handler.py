# import json
# import threading

# class ClientHandler(threading.Thread):
#     def __init__(self, socket, address, queue, contest_manager):
#         super().__init__(daemon=True)
#         self.socket = socket
#         self.address = address
#         self.queue = queue
#         self.contest_manager = contest_manager

#     def run(self):
#         while True:
#             try:
#                 raw = self.socket.recv(100000).decode().strip()
#                 if not raw:
#                     break

#                 data = json.loads(raw)

#                 if data["type"] == "submit":

#                     if not self.contest_manager.contest_active():
#                         self.socket.send(b"Contest finished\n")
#                         continue

#                     self.queue.push({
#                         "username": data["username"],
#                         "problem_id": data["problem_id"],
#                         "language": data["language"],
#                         "code": data["code"],
#                         "client_socket": self.socket
#                     })

#                     self.socket.send(b"Submission received\n")

#             except:
#                 break


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

                # 🔥 TASK SANS SOCKET (pickle-safe)
                task = {
                    "username": data["username"],
                    "problem_id": data["problem_id"],
                    "language": data["language"],
                    "code": data["code"],
                }

                # socket stocké à côté
                self.queue.push((task, self.socket))

                # première réponse
                self.socket.send(b"Submission received\n")
                return

        except Exception:
            return
