[![Coverage Status](https://codecov.io/gh/tembici/temlogger/branch/master/graph/badge.svg)](https://codecov.io/gh/tembici/temlogger)

# TemLogger
**Temlogger** is a library to send logs to ELK, StackDriver(Google Cloud Logging).

## Features

Temlogger gives you:

* Flexibility to send logs to StackDriver(Google Cloud Logging) or ELK (Elastic, Logstash and Kibana).
* Register events handlers(globally and per logger) to update log entry before send to providers.
* 98% test coverage.

## Logging Providers

* `logstash` (ELK)
* `stackdriver` (Google StackDriver)
* `default` (don't send logs)


## Requirements
* python 3.6+
* python3-logstash == 0.4.80
* google-cloud-logging>=1.14.0,<2

## Instalation

    pip install temlogger


## Usage

### How to use temlogger

#### Can be used with environment variables:

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

#### Can be used with explict parameters:

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

### Parameters to use with Logstash

    export TEMLOGGER_PROVIDER='logstash'
    export TEMLOGGER_URL='<logstash url>'
    export TEMLOGGER_PORT='<logstash port>'
    export TEMLOGGER_ENVIRONMENT='<your environment>'


### Parameters to use with StackDriver
The variable `GOOGLE_APPLICATION_CREDENTIALS` is now deprecated and your use isn't recommended. Use `TEMLOGGER_GOOGLE_CREDENTIALS_BASE64` instead. 

    export TEMLOGGER_PROVIDER='stackdriver'
    export TEMLOGGER_ENVIRONMENT='<your environment>'
    export TEMLOGGER_GOOGLE_CREDENTIALS_BASE64='<your google json creds as base64>'

To encode your google credentials use:

```bash
base64 <google application credentials path>
```

### Example with StackDriver

If you have a Google Credentials, step ahead. If not, create one here https://console.cloud.google.com/apis/credentials/serviceaccountkey. It's recomended to assign just the needed permissions (`logging > write logs`).
```bash
export TEMLOGGER_PROVIDER='stackdriver'
export TEMLOGGER_GOOGLE_CREDENTIALS_BASE64='<your google json creds as base64>'
```

```python
import sys
import temlogger

logger = temlogger.getLogger('python-stackdriver-logger')

logger.info('python-stackdriver: test stackdriver info message.')

# add extra field to stackdriver message
extra = {
    'test_string': 'python version: ' + repr(sys.version_info),
    'test_boolean': True,
    'test_dict': {'a': 1, 'b': 'c'},
    'test_float': 1.23,
    'test_integer': 123,
    'test_list': [1, 2, '3'],
}
logger.info('temlogger: test with extra fields', extra=extra)
```

### Example with LogStash

```bash
export TEMLOGGER_PROVIDER='logstash'
export TEMLOGGER_URL='localhost'
export TEMLOGGER_PORT='5000'
export TEMLOGGER_ENVIRONMENT='staging'
```

```python
import sys
import temlogger

logger = temlogger.getLogger('python-logstash-logger')

logger.info('python-logstash: test logstash info message.')

# add extra field to stackdriver message
extra = {
    'test_string': 'python version: ' + repr(sys.version_info),
    'test_boolean': True,
    'test_dict': {'a': 1, 'b': 'c'},
    'test_float': 1.23,
    'test_integer': 123,
    'test_list': [1, 2, '3'],
}
logger.info('temlogger: test with extra fields', extra=extra)
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

## Event Handlers

This functionality allow register handlers before send log to Logging Providers.

### Register event handlers globally

Is recommended initialize event handlers early as possible, for example in `settings.py` for django.
The below example shows how register a handler `add_tracker_id_to_message` globally.

```python
import temlogger

temlogger.config.set_provider('logstash')
temlogger.config.setup_event_handlers([
    'temlogger.tests.base.add_tracker_id_to_message',
])

logger = temlogger.getLogger('python-logger')

extra = {
    'app_name': 'tembici'
}

logger.info('test with extra fields', extra=extra)
```

### Register event handlers per logger

The below example shows how register a handler `add_user_id_key` for one logger.

```python
import temlogger

def add_user_id_key(message):
    message['user_id'] = 'User Id'
    return message

temlogger.config.set_provider('logstash')

logger = temlogger.getLogger('python-logger', event_handlers=[
    'temlogger.tests.base.add_tracker_id_to_message',
    add_user_id_key
])
extra = {
    'app_name': 'tembici'
}

logger.info('test with extra fields', extra=extra)
```