install:
	python3 setup.py install
	http-log-monitor --file="/tmp/access.log"


test:
	python3 -m unittest
