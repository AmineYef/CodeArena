import queue
import threading

class TaskQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.lock = threading.Lock()

    def push(self, task):
        with self.lock:
            self.queue.put(task)

    def pop(self):
        with self.lock:
            if self.queue.empty():
                return None
            return self.queue.get()

    def size(self):
        return self.queue.qsize()
