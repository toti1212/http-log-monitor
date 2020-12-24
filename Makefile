install:
	python3 setup.py install

test:
	python3 -m unittest

monitor:
	http-log-monitor --file="/tmp/access.log" --interval 10 --alert_trigger 10 --alert_time_window 120 

simulator:
	http-log-simulator --wait_between 90