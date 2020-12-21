from threading import Thread
from queue import Queue
from time import time


class Stats(Thread):
    def __init__(self, log_entries_queue: Queue, threadhold: int):
        super().__init__()

        self.log_entries_queue = log_entries_queue
        self.threadhold = threadhold

    def run(self):
        last_stats_ts = time()

        while True:
            if time() - last_stats_ts >= self.threadhold:
                stats = self.generate_stats()

    def generate_stats(self):
        print("todo")
