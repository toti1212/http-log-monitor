import unittest
from queue import Queue
import time
from http_log_monitor.displays.cli import Cli
from http_log_monitor.monitoring.alert import AlertMonitor
from http_log_monitor.simulator import LogGenerator
from datetime import datetime


class TestAlertMonitor(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()
        self.display = Cli(disable_print_welcome_msg=True)
        self.trigger = 5  # request / second
        self.time_window = 5  # seconds

        self.alertMonitor = AlertMonitor(
            alert_queue=self.queue,
            display=self.display,
            trigger=self.trigger,
            time_window=self.time_window,
        )

        # log generator
        self.log_entry = {
            "remote_host": "localhost",
            "user_id": "-",
            "user_name": "user2",
            "datetime": datetime.now().strftime("%d/%b/%Y:%X"),
            "response_type": "200",
            "response_size": "499",
            "method": "GET",
            "resource": "/orders/pages=1",
            "protocol": "HTTP/1.0",
            "resource_base_path": "/orders",
        }

    def test_alert_rise(self):
        self.alertMonitor.start()
        self.alertMonitor.alert_queue.put(self.log_entry)

        self.assertFalse(self.alertMonitor.alert_active)

        # populate the queue with logs
        for i in range(50):
            self.alertMonitor.alert_queue.put(self.log_entry)

        time.sleep(0.1)
        self.assertTrue(self.alertMonitor.alert_active)

        time.sleep(self.time_window)
        self.assertFalse(self.alertMonitor.alert_active)


if __name__ == "__main__":
    unittest.main()
