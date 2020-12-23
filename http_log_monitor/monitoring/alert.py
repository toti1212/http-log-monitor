from threading import Thread, Lock
import time
from typing import List
from http_log_monitor.displays.display import Display
from enum import Enum
from queue import Queue
from datetime import datetime


class AlertType(Enum):
    HIGH_TRAFFIC = 1
    RECOVER = 2


class Alert:
    def __init__(self, type: AlertType, timestamp, hits=None):
        self.type = type
        self.hits = hits
        self.timestamp = timestamp


class AlertMonitor(Thread):
    def __init__(
        self, alert_queue: Queue, display: Display, time_window: int, trigger: int
    ):
        super().__init__()
        self.daemon = True

        self.alert_queue = alert_queue
        self.alert_active = False
        self.alert_list = []
        self.display = display
        self.trigger = trigger
        self.time_window = time_window

    def run(self):
        while True:
            self._update_alert_list()
            hits = len(self.alert_list)

            if not self.alert_active and hits / self.time_window > self.trigger:
                self.display.set_alert(
                    Alert(AlertType.HIGH_TRAFFIC, datetime.now(), hits)
                )
                self.alert_active = True

            elif self.alert_active and hits / self.time_window < self.trigger:
                self.display.set_alert(Alert(AlertType.RECOVER, datetime.now(), None))
                self.alert_active = False

            self.watch_alert_list_time_window()
            time.sleep(0.25)

    def watch_alert_list_time_window(self):
        while not self.alert_queue.empty():
            entry = self.alert_queue.get()
            self.alert_list.append(entry)
            self._update_alert_list()

    def _update_alert_list(self):
        """
        Time window algorithm.
        We need to keep only the entries that are useful in the time_window interval.
        """
        # TODO: Improve datetimes
        current_ts = datetime.now()
        for entry in self.alert_list:
            entry_ts = datetime.strptime(entry.get("datetime"), "%d/%b/%Y:%X")
            if (current_ts - entry_ts).total_seconds() > self.time_window:
                self.alert_list.remove(entry)

