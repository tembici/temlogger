[![Coverage Status](https://codecov.io/gh/tembici/temlogger/branch/master/graph/badge.svg)](https://codecov.io/gh/tembici/temlogger)

# TemLogger
**Temlogger** is a library to capture and send logs to ELK, StackDriver.

## Logging Providers

* `logstash` (ELK)
* `stackdriver` (Google StackDriver)
* `default` (don't send logs)


## Requirements
* python 3.6+
* python3-logstash == 0.4.80
* google-cloud-logging>=1.14.0,<2

## Instalation

    pip install -e git+https://github.com/tembici/temlogger.git#egg=temlogger

Use this to specify tag version:

    pip install -e git+https://github.com/tembici/temlogger.git@<tag-version>#egg=temlogger


## Usage

Using environment variables:

```bash
export TEMLOGGER_PROVIDER='logstash'
export TEMLOGGER_URL='localhost'
export TEMLOGGER_PORT='5000'
export TEMLOGGER_ENVIRONMENT='staging'
```

```python
import sys
import temlogger

test_logger = temlogger.getLogger('python-logstash-logger')

test_logger.error('python-logstash: test logstash error message.')
test_logger.info('python-logstash: test logstash info message.')
test_logger.warning('python-logstash: test logstash warning message.')

# add extra field to logstash message
extra = {
    'test_string': 'python version: ' + repr(sys.version_info),
    'test_boolean': True,
    'test_dict': {'a': 1, 'b': 'c'},
    'test_float': 1.23,
    'test_integer': 123,
    'test_list': [1, 2, '3'],
}
test_logger.info('temlogger: test with extra fields', extra=extra)
```

Example passing parameters directly to temlogger:

```python
import sys
import temlogger

temlogger.config.set_provider('logstash')
temlogger.config.set_url('localhost')
temlogger.config.set_port(5000)
temlogger.config.set_environment('staging')

test_logger = temlogger.getLogger('python-logstash-logger')

test_logger.info('python-logstash: test logstash info message.')

# add extra field to logstash message
extra = {
    'test_string': 'python version: ' + repr(sys.version_info),
    'test_boolean': True,
    'test_dict': {'a': 1, 'b': 'c'},
    'test_float': 1.23,
    'test_integer': 123,
    'test_list': [1, 2, '3'],
}
test_logger.info('temlogger: test with extra fields', extra=extra)
```

### Example with StackDriver

```bash
export TEMLOGGER_PROVIDER='stackdriver'
# https://cloud.google.com/docs/authentication/getting-started
export GOOGLE_APPLICATION_CREDENTIALS='<path to json>'
```

```python
import sys
import temlogger

test_logger = temlogger.getLogger('python-stackdriver-logger')

test_logger.info('python-stackdriver: test stackdriver info message.')

# add extra field to stackdriver message
extra = {
    'test_string': 'python version: ' + repr(sys.version_info),
    'test_boolean': True,
    'test_dict': {'a': 1, 'b': 'c'},
    'test_float': 1.23,
    'test_integer': 123,
    'test_list': [1, 2, '3'],
}
test_logger.info('temlogger: test with extra fields', extra=extra)
```

### Using with Django

Modify your `settings.py` to integrate temlogger with Django's logging:

```python
import temlogger

host = 'localhost'

temlogger.config.set_provider('logstash')
temlogger.config.set_url('localhost')
temlogger.config.set_port(5000)
temlogger.config.set_environment('staging')

```

Then in others files such as `views.py`,`models.py` you can use in this way:

```python
import temlogger

test_logger = temlogger.getLogger('python-logger')
```
