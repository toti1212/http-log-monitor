import os
import time
from datetime import datetime
from subprocess import call

from http_log_monitor.monitoring.alert import Alert, AlertType

from .display import Display


class Cli(Display):
    """Command line display.
    Show the stats and alarms in the CLI printing the data an cleaning the screen"""

    BOLD_TEXT = "\033[1m"
    RESET_TEXT = "\033[0m"
    WELCOME_MSG = " HTTP log monitor program "
    LINE_SEPARATOR = f"{'-'* len(WELCOME_MSG)}"
    DATE_FORMAT = "%H:%M:%S"
    REFRESH_INTERVAL = 100  # milliseconds

    def __init__(self):
        super().__init__()
        self.alert = None
        # Starting the display printing the welcome msg
        self._clear()
        self._print_welcome_msg()

    def run(self):
        while True:
            # Refresh the screen every second
            self.refresh_screen()
            time.sleep(1)

    def _print_welcome_msg(self):
        print(self._bold(self.LINE_SEPARATOR))
        print(self._bold(self.WELCOME_MSG))
        print(self._bold(self.LINE_SEPARATOR))

    def _bold(self, text):
        """Format the text to bold (terminal supported)"""
        return f"{self.BOLD_TEXT}{text}{self.RESET_TEXT}"

    def _clear(self):
        """Clean the screen. OS compatibility"""
        _ = call("clear" if os.name == "posix" else "cls", shell=True)

    def refresh_screen(self):
        """Main function that refresh the screen with new stats and/or alarms"""
        self._clear()
        self._print_welcome_msg()

        self.print_alert()
        self.print_stats()

    def set_stats(self, stats: dict):
        self.stats = stats

    def set_alert(self, alert: Alert):
        self.alert = alert

    def print_alert(self):
        """Depends of the alert type, a text is displayed on the main screen"""
        msg = ""
        if self.alert and self.alert.type == AlertType.HIGH_TRAFFIC:
            msg = f"High traffic generated an alert - hits = {self.alert.hits}, triggered at {self.alert.timestamp}"
        elif self.alert and self.alert.type == AlertType.RECOVER:
            msg = (
                f"High traffic alert disabled. Back to normal at {self.alert.timestamp}"
            )
        print(self._bold(msg))

    def print_stats(self):
        """Displays stats in a nice way"""
        # TODO: improve real time updates
        print(f"{self._bold('Time:')} {datetime.now().strftime(self.DATE_FORMAT)}")
        print(f"{self._bold('Log path:')} {self.stats.get('log_path')}")
        print(f"{self._bold('Interval:')} {self.stats.get('interval')} seg")
        print(f"{self._bold('Total hits:')} {self.stats.get('total_logs_read', 0)}")
        print(f"{self._bold('Hits/sec:')} {self.stats.get('hits_per_sec', 0)}")
        if self.stats.get("top_hits"):
            print(f"{self._bold('Top hits:')}")
            print(f"{self._bold('Hits')} \t {self._bold('Resource')}")

            # TODO: Improve tabs and aligns
            for k, v in self.stats.get("top_hits"):
                print(f"{v} \t {k}")

