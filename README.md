# TemLogger
**Temlogger** is a library with a purpose to capture and save all logs. This lib was composed Elasticsearch, Logstash, Kibana and created one more condition to attach with stackdrive from google in the future.

## Logging Providers

* `logstash` (ELK)
* `stackdriver` (Google StackDriver)
* `default` (don't send logs)


## Requirements
* python 3.6+
* python3-logstash == 0.4.80
* google-cloud-logging >= 1.14.0,<2

## Instalation

    pip install -e git+https://git.repo/some_pkg.git#egg=SomeProject

## Examples
**Create it**
	Create a file main.py with:
		import temlogger
