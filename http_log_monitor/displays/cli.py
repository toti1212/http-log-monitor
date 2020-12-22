from subprocess import call
from .display import Display
from datetime import datetime
import os


class Cli(Display):
    BOLD_TEXT = "\033[1m"
    RESET_TEXT = "\033[0m"
    WELCOME_MSG = " HTTP log monitor program "
    LINE_SEPARATOR = f"{'-'* len(WELCOME_MSG)}"

    def __init__(self):
        super().__init__()

        # Welcome msg
        self._clear()
        self._print_welcome_msg()

    def _print_welcome_msg(self):
        print(self._bold(self.LINE_SEPARATOR))
        print(self._bold(self.WELCOME_MSG))
        print(self._bold(self.LINE_SEPARATOR))

    def _bold(self, text):
        return f"{self.BOLD_TEXT}{text}{self.RESET_TEXT}"

    def _clear(self):
        _ = call("clear" if os.name == "posix" else "cls")

    def show_data(self, data: dict):
        """
        """
        self._clear()
        self._print_welcome_msg()
        # TODO: improve real time updates
        print(f"{self._bold('Time:')} {datetime.now().strftime('%H:%M:%S')}")
        print(f"{self._bold('Log path:')} {data.get('log_path')}")
        print(f"{self._bold('Threadhold:')} {data.get('threadhold')} seg")
        print(f"{self._bold('Total hits:')} {data.get('total_logs_read', 0)}")
        if data.get("top_hits"):
            print(f"{self._bold('Top hits:')}")
            print(f"{self._bold('Hits')} \t {self._bold('Resource')}")

            # TODO: Improve tabs and aligns
            for k, v in data.get("top_hits"):
                print(f"{v} \t {k}")

