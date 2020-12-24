# 📈 http-log-monitor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

HTTP log monitor CLI to monitor log files, view stats and track alarms when traffic exceeds a certain threshold.

## Requirements

This library was thought and designed from the beginning to **not use** **any dependencies** (in principle). So the prerequisites are quite simple.

- Python 3.x

## Installation

There are basically two main commands located in `/bin` which are:

`http-log-monitor`

`http-log-simulator`

The library has a `Makefile` file which has essential shortcuts / commands to run the most important modules. Basically to run it you have to run

```bash
make install
```

## Usage

### How to use it

Once installed, you can start to monitoring a log file executing:

```bash
http-log-monitor --file <path>
```

Also, if you want to execute with the default values you can run `make monitor`

On the other hand, if you want to use the simulator script, you can execute:

```bash
http-log-simulator --output <path> --wait_between 100
```

As the monitor script, if you want to execute with the default values you can run `make simulator`

---

### Monitor

`http-log-monitor`

```makefile
usage: http-log-monitor [-h] [--file FILE] [--interval INTERVAL]
                        [--alert_trigger ALERT_TRIGGER]
                        [--alert_time_window ALERT_TIME_WINDOW]

optional arguments:
  -h, --help            show this help message and exit
  --file FILE           file to monitoring
  --interval INTERVAL   interval where statistics are updated. Default 10 seg
  --alert_trigger ALERT_TRIGGER requests trigger to show an alert for high traffic. Default 10 req/seg
  --alert_time_window ALERT_TIME_WINDOW time windows to monitor the alarms. Default 120 seg
```


_See code: [bin/http-log-monitor](https://github.com/toti1212/http-log-monitor/blob/main/bin/http-log-monitor)_

### Simulator

`http-log-simulator`

```makefile
usage: http-log-simulator [-h] [--output OUTPUT] [--wait_between WAIT_BETWEEN]

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT       Log file to create. Default /tmp/access.log
	--wait_between WAIT_BETWEEN
												Seconds between the next fake log entry. Default 100 ms
```

_See code: [](https://github.com/toti1212/http-log-monitor/blob/main/bin/http-log-monitor)[bin/http-log-simulator](https://github.com/toti1212/http-log-monitor/blob/main/bin/http-log-simulator)_

## Design

---

### Reader

The reader module goes through the log entries and saves them in two queues, one for analyzing the stats and the other for the alarms.

### Monitoring

Inside this folder are the different types of monitors that we can have. In this case, we are going to monitor the statistics and alarms.

### Display

The display module is the module in charge of displaying / sending the information received and managed by the monitors. In this case, we have a `CLI` display instantiated which refreshes the screen every second and shows the information and alarms.

## Improvements

---

- Use a pub / sub architecture to be able to decouple responsibilities in the code and to be able to use event-based programming
- Add more stats like: top errors, bandwidth, etc.
- Add more alarm types: rate of errors, suspicious `remote_host`, etc.
- Improve the way information is displayed. Use a library like [curses](https://docs.python.org/3/library/curses.html) in python to be able to create 2 columns that refresh in real time.
- Create export modules to add integrations with services that can receive this information (such as Datadog)
- Be able to create / generate a python library to be installed with a package manager such as `pip` or`Poetry`
- Add pipelines to run tests and create a new version when merged with the main
- Improve test coverage

## License

---

This package is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).
