from threading import Thread
from queue import Queue
from time import time
from http_log_monitor.displays.display import Display


class StatsMonitor(Thread):
    def __init__(
        self, queue: Queue, display: Display, log_path: str, interval: int = 10
    ):
        super().__init__()
        self.daemon = True
        self.queue = queue
        self.display = display
        self.log_path = log_path
        self.interval = interval
        self.total_logs_read = 0

    def run(self):
        last_stats_ts = 0

        while True:

            if time() - last_stats_ts >= self.interval:
                self.total_logs_read = 0
                stats = self.generate_stats()
                last_stats_ts = time()
                self.display.set_stats(stats)

    def _get_dict_from_entries(self):
        entries = {}

        while not self.queue.empty():
            # Get all log entries and count the base path hits
            entry = self.queue.get()
            self.total_logs_read += 1
            base_path = entry.get("resource_base_path")
            if not entries.get(base_path):
                entries[base_path] = 1
            else:
                entries[base_path] += 1

        return entries

    def generate_stats(self) -> dict:
        data = self._get_dict_from_entries()

        top_hits = None
        if data:
            top_hits = list(sorted(data.items(), key=lambda item: item[1], reverse=True))[:3]
        
        stats = {
            "log_path": self.log_path,
            "top_hits": top_hits,
            "total_logs_read": self.total_logs_read,
            "interval": self.interval,
        }

        return stats

