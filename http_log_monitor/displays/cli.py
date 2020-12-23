from http_log_monitor.monitoring.alert import Alert, AlertType
from subprocess import call
from .display import Display
from datetime import datetime
import os

import time


class Cli(Display):
    BOLD_TEXT = "\033[1m"
    RESET_TEXT = "\033[0m"
    WELCOME_MSG = " HTTP log monitor program "
    LINE_SEPARATOR = f"{'-'* len(WELCOME_MSG)}"
    DATE_FORMAT = "%H:%M:%S"
    REFRESH_INTERVAL = 100  # milliseconds

    def __init__(self):
        super().__init__()
        self.alert = None
        
        # Welcome msg
        self._clear()
        self._print_welcome_msg()

    def run(self):
        while True:
            self.refresh_screen()
            time.sleep(1)

    def _print_welcome_msg(self):
        print(self._bold(self.LINE_SEPARATOR))
        print(self._bold(self.WELCOME_MSG))
        print(self._bold(self.LINE_SEPARATOR))

    def _bold(self, text):
        return f"{self.BOLD_TEXT}{text}{self.RESET_TEXT}"

    def _clear(self):
        _ = call("clear" if os.name == "posix" else "cls", shell=True)

    def refresh_screen(self):
        self._clear()
        self._print_welcome_msg()

        self.print_alert()
        self.print_stats()

    def set_stats(self, stats: dict):
        self.stats = stats

    def set_alert(self, alert: Alert):
        self.alert = alert

    def print_alert(self):
        msg = ""
        if self.alert and self.alert.type == AlertType.HIGH_TRAFFIC:
            msg = f"High traffic generated an alert - hits = {self.alert.hits}, triggered at {self.alert.timestamp}"
        elif self.alert and self.alert.type == AlertType.RECOVER:
            msg = f"Traffic on normal params"
        print(self._bold(msg))

    def print_stats(self):
        # TODO: improve real time updates
        print(f"{self._bold('Time:')} {datetime.now().strftime(self.DATE_FORMAT)}")
        print(f"{self._bold('Log path:')} {self.stats.get('log_path')}")
        print(f"{self._bold('Interval:')} {self.stats.get('interval')} seg")
        print(f"{self._bold('Total hits:')} {self.stats.get('total_logs_read', 0)}")
        if self.stats.get("top_hits"):
            print(f"{self._bold('Top hits:')}")
            print(f"{self._bold('Hits')} \t {self._bold('Resource')}")

            # TODO: Improve tabs and aligns
            for k, v in self.stats.get("top_hits"):
                print(f"{v} \t {k}")

