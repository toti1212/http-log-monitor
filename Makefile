install:
	python3 setup.py install
	http-log-monitor --file="/tmp/access.log" --interval 10 --alert_trigger 10 --alert_time_window 120 


test:
	python3 -m unittest
