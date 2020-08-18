|Coverage Status|

TemLogger
=========

**Temlogger** is a library to sends logs to providers such as ELK and
StackDriver(Google Cloud Logging). Temlogger can be used in any python
3.6+ application.

Features
--------

Temlogger gives you:

-  Flexibility to send logs:

   -  StackDriver(Google Cloud Logging)
   -  ELK (Elastic, Logstash and Kibana)
   -  Console (Default logging output)

-  Register events handlers(globally and per logger) to update log entry
   before send to providers.
-  99% test coverage.

Logging Providers
-----------------

-  ``logstash`` (ELK)
-  ``stackdriver`` (Google StackDriver)
-  ``console`` (Display logs on Console)
-  ``default`` (don’t send logs)

Requirements
------------

-  python 3.6+
-  python3-logstash == 0.4.80
-  google-cloud-logging>=1.14.0,<2

Instalation
-----------

::

   pip install temlogger

Configuration
-------------

Temlogger can be used with environment variables or programmatically.

Example of configuration with environment variables to Console provider:

.. code:: bash

   export TEMLOGGER_APP_NAME='your-app-name'
   export TEMLOGGER_PROVIDER='console'
   export TEMLOGGER_ENVIRONMENT='staging'
   export TEMLOGGER_LOG_LEVEL='INFO'

.. code:: python

   import sys
   import temlogger

   test_logger.info('python-console: test console info message.')
   test_logger.debug('python-console: debug message will not be displayed. Change level to "DEBUG"')
   test_logger.warning('python-console: test console warning message.')

Example of configuration programmatically to Console provider:

.. code:: python

   import sys
   import temlogger

   temlogger.config.set_app_name('your-app-name')
   temlogger.config.set_provider('console')
   temlogger.config.set_environment('staging')
   temlogger.config.set_log_level('INFO')

   test_logger.info('python-console: test console info message.')
   test_logger.debug('python-console: debug message will not be displayed. Change level to "DEBUG"')
   test_logger.warning('python-console: test console warning message.')

Parameters to setup Logstash Provider
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   export TEMLOGGER_APP_NAME='your-app-name'
   export TEMLOGGER_PROVIDER='logstash'
   export TEMLOGGER_URL='<logstash url>'
   export TEMLOGGER_PORT='<logstash port>'
   export TEMLOGGER_ENVIRONMENT='<your environment>'
   export TEMLOGGER_LOG_LEVEL='INFO'

Parameters to setup StackDriver Provider
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The variable ``GOOGLE_APPLICATION_CREDENTIALS`` is now deprecated and
your use isn’t recommended. Use ``TEMLOGGER_GOOGLE_CREDENTIALS_BASE64``
instead.

::

   export TEMLOGGER_APP_NAME='your-app-name'
   export TEMLOGGER_PROVIDER='stackdriver'
   export TEMLOGGER_ENVIRONMENT='<your environment>'
   export TEMLOGGER_GOOGLE_CREDENTIALS_BASE64='<your google json creds as base64>'
   export TEMLOGGER_LOG_LEVEL='INFO'

To encode your google credentials use:

.. code:: bash

   base64 <google application credentials path>

Parameters to setup Console Provider
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   export TEMLOGGER_PROVIDER='console'
   export TEMLOGGER_ENVIRONMENT='<your environment>'
   export TEMLOGGER_LOG_LEVEL='INFO'

Usage Examples
--------------

Example with StackDriver
~~~~~~~~~~~~~~~~~~~~~~~~

If you have a Google Credentials, step ahead. If not, create one here
https://console.cloud.google.com/apis/credentials/serviceaccountkey.
It’s recomended to assign just the needed permissions
(``logging > write logs``).

.. code:: bash

   export TEMLOGGER_APP_NAME='your-app-name'
   export TEMLOGGER_PROVIDER='stackdriver'
   export TEMLOGGER_GOOGLE_CREDENTIALS_BASE64='<your google json creds as base64>'
   export TEMLOGGER_ENVIRONMENT='staging'
   export TEMLOGGER_LOG_LEVEL='INFO'

.. code:: python

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

Example with LogStash
~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   export TEMLOGGER_APP_NAME='your-app-name'
   export TEMLOGGER_PROVIDER='logstash'
   export TEMLOGGER_URL='localhost'
   export TEMLOGGER_PORT='5000'
   export TEMLOGGER_ENVIRONMENT='staging'
   export TEMLOGGER_LOG_LEVEL='INFO'

.. code:: python

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

Example with Console
~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   export TEMLOGGER_APP_NAME='your-app-name'
   export TEMLOGGER_PROVIDER='console'
   export TEMLOGGER_ENVIRONMENT='staging'
   export TEMLOGGER_LOG_LEVEL='INFO'

.. code:: python

   import sys
   import temlogger

   logger = temlogger.getLogger('python-console-logger')

   logger.info('python-logstash: test logstash info message.')

   # add extra field to log message
   extra = {
       'test_string': 'python version: ' + repr(sys.version_info),
       'test_boolean': True,
       'test_dict': {'a': 1, 'b': 'c'},
   }
   logger.info('temlogger: test with extra fields', extra=extra)

Using with Django
~~~~~~~~~~~~~~~~~

Modify your ``settings.py`` to integrate temlogger with Django’s
logging:

.. code:: python

   import temlogger

   host = 'localhost'

   temlogger.config.set_app_name('your-app-name')
   temlogger.config.set_provider('logstash')
   temlogger.config.set_url('localhost')
   temlogger.config.set_port(5000)
   temlogger.config.set_environment('staging')
   temlogger.config.set_log_level('INFO')

Then in others files such as ``views.py``,\ ``models.py`` you can use in
this way:

.. code:: python

   import temlogger

   test_logger = temlogger.getLogger('python-logger')

Event Handlers
--------------

This functionality allow register handlers before send log to Logging
Providers.

Register event handlers globally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Is recommended initialize event handlers early as possible, for example
in ``settings.py`` for django. The below example shows how register a
handler ``add_tracker_id_to_message`` globally.

.. code:: python

   import temlogger

   temlogger.config.set_app_name('your-app-name')
   temlogger.config.set_provider('console')
   temlogger.config.set_log_level('INFO')

   temlogger.config.setup_event_handlers([
       'temlogger.tests.base.add_tracker_id_to_message',
   ])

   logger = temlogger.getLogger('python-logger')

   extra = {
       'app_name': 'tembici'
   }

   logger.info('test with extra fields', extra=extra)

Register event handlers per logger
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The below example shows how register a handler ``add_user_id_key`` for
one logger.

.. code:: python

   import temlogger

   def add_user_id_key(message):
       message['user_id'] = 'User Id'
       return message

   temlogger.config.set_app_name('your-app-name')
   temlogger.config.set_provider('console')
   temlogger.config.set_log_level('INFO')

   logger = temlogger.getLogger('python-logger', event_handlers=[
       'temlogger.tests.base.add_tracker_id_to_message',
       add_user_id_key
   ])
   extra = {
       'app_name': 'tembici'
   }

   logger.info('test with extra fields', extra=extra)

.. |Coverage Status| image:: https://codecov.io/gh/tembici/temlogger/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/tembici/temlogger
