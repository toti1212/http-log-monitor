import random
from datetime import datetime
from random import choice, randint
from time import gmtime, strftime

class LogGenerator:
    def generate_log_entry(self):
        log_line = (
            f"{self._generate_remote_host()} "
            f"{self._generate_user_id()} "
            f"{self._generate_user_name()} "
            f"[{self._generate_date()}] "
            f'"{self._generate_request_method()} {self._generate_request_resource()} {self._generate_request_protocol()}" '
            f"{self._generate_response_type()} {self._generate_response_bytes()} \n"
        )
        return log_line

    def _generate_remote_host(self):
        return "localhost"

    def _generate_user_id(self):
        return "-"

    def _generate_user_name(self) -> str:
        return choice(["user1", "user2", "user3"])

    def _generate_date(self) -> str:
        return f"{datetime.now().strftime('%d/%b/%Y:%X')}"

    def _generate_request_method(self) -> str:
        return choice(["GET", "POST", "PUT", "PATCH"])

    def _generate_request_resource(self) -> str:
        return choice(
            [
                "/",
                "/users/1",
                "/orders/pages=1",
                "/customers" "/customers/1/edit",
                "/login",
            ]
        )

    def _generate_request_protocol(self) -> str:
        return "HTTP/1.0"

    def _generate_response_type(self) -> str:
        return str(choice([200, 201, 300, 301, 302, 400, 404, 500]))

    def _generate_response_bytes(self) -> str:
        return str(randint(50, 500))
