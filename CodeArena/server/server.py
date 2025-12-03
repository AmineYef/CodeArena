import socket
import threading

from server.settings import SERVER_HOST, SERVER_PORT, MAX_CLIENTS
from server.queue_manager import TaskQueue
from server.leaderboard import Leaderboard
from server.contest_manager import ContestManager
from server.dispatcher import Dispatcher
from server.client_handler import ClientHandler


def start_server():
    contest = ContestManager()
    queue = TaskQueue()
    leaderboard = Leaderboard()

    contest.create_contest(num_problems=1, difficulty="easy")

    dispatcher = Dispatcher(queue, leaderboard, contest)
    dispatcher.start()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(MAX_CLIENTS)

    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    try:
        while True:
            client_socket, addr = server.accept()
            handler = ClientHandler(client_socket, addr, queue, contest)
            handler.start()

    except KeyboardInterrupt:
        print("\n[SERVER] Stopping server gracefully...")
        server.close()


if __name__ == "__main__":  
    start_server()
