"""Reader"""

from threading import Thread
from os import SEEK_END
import re
import time
from queue import Queue



class Reader(Thread):
    """
    Reader module.
    This will watch the a resource constantly and saving the information
    to analyze later.
    """

    def __init__(self, file_path: str, queue: Queue):
        super().__init__()
        self.daemon = True
        self.file_path = file_path
        self.queue = queue

    def run(self):
        file = open(self.file_path, "r")
        file.seek(0, 2)

        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)
            else:
                try:
                    parsed_log_line = self.parse_log_line(line)
                    self.queue.put(parsed_log_line)
                except Exception as e:
                    #  TODO: Improve logs
                    print(e)
                    raise

    def parse_log_line(self, line: str):
        # parse log
        try:
            parsed_log_line = self._parse_log_entry(line)

            parsed_request = self._parse_request_entry(parsed_log_line.pop("request"))
            parsed_log_line.update(parsed_request)

            parsed_request_resource = self._parse_request_resource_entry(
                parsed_request.get("resource")
            )
            parsed_log_line.update({"resource_base_path": parsed_request_resource})

            return parsed_log_line
        except Exception as e:
            # TODO: Improve logs
            print(f"Cannot parse log: {e}")
            raise

    def _parse_log_entry(self, line: str) -> dict:
        log_parts = [
            r"(?P<remote_host>\S*)",
            r"(?P<user_id>\S*)",
            r"(?P<user_name>\S*)",
            r"\[(?P<datetime>.*?)\]",
            r'"(?P<request>.+)"',
            r"(?P<response_type>\d*)",
            r"(?P<response_size>\d*)",
        ]

        log_pattern = re.compile(r"\s+".join(log_parts) + r"\s*")
        matching_pattern_log = log_pattern.match(line)
        return matching_pattern_log.groupdict()

    def _parse_request_entry(self, request_line: str) -> dict:
        request_parts = [r"(?P<method>\S+)", r"(?P<resource>\S+)", r"(?P<protocol>\S+)"]
        request_pattern = re.compile(r"\s+".join(request_parts) + r"\s*")
        matching_pattern_request = request_pattern.match(request_line)
        return matching_pattern_request.groupdict()

    def _parse_request_resource_entry(self, request_resource: str) -> str:
        parsed_request_resource = request_resource.split("/")
        if len(parsed_request_resource) <= 1:
            return ""
        if parsed_request_resource[1] == "":
            return "/"
        return f"/{parsed_request_resource[1]}"
