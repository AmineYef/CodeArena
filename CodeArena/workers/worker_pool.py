from multiprocessing import Pool
from server.settings import NUM_WORKERS
from workers.worker_process import worker_process

class WorkerPool:
    def __init__(self):
        self.pool = Pool(NUM_WORKERS)

    def execute(self, task):
        async_res = self.pool.apply_async(worker_process, (task,))
        return async_res.get()
    def close(self):
        self.pool.close()
        self.pool.terminate()
        self.pool.join()
