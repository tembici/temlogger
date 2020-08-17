import logging
import os
import unittest
import temlogger

from unittest import mock

from .base import clean_temlogger_config
from .base import VALID_GOOGLE_CREDENTIALS
from ..helpers import encode_file_as_base64


class TestDefaultLogger(unittest.TestCase):

    def setUp(self):
        """
        Clean config between tests
        """
        clean_temlogger_config()

    def test_get_default_logger_when_logging_provider_is_not_set(self):
        logger = temlogger.getLogger('test')

        self.assertTrue(isinstance(logger, logging.Logger))
        self.assertEqual(logger.logging_provider, 'default')
        self.assertEqual(len(logger.handlers), 0)

    def test_defaultlogger_with_app_name(self):
        default_app_name = 'stackdriver-app'

        temlogger.config.set_provider('default-app_name')
        temlogger.config.set_app_name(default_app_name)

        self.assertEqual(temlogger.config.get_app_name(), default_app_name)

    def test_defaultlogger_with_app_name_as_environment(self):
        default_app_name = 'stackdriver-app'

        os.environ['TEMLOGGER_APP_NAME'] = default_app_name

        temlogger.config.set_provider('default')

        self.assertEqual(temlogger.config.get_app_name(), default_app_name)


class TestLogstashLogger(unittest.TestCase):

    def setUp(self):
        """
        Clean config between tests
        """
        clean_temlogger_config()

    def test_switch_logger(self):
        logger = temlogger.getLogger('switch-logger-1')
        self.assertTrue(isinstance(logger, logging.Logger))
        self.assertEqual(logger.logging_provider, 'default')

        temlogger.config.set_provider('logstash')
        logger = temlogger.getLogger('switch-logger-1')
        self.assertTrue(isinstance(logger, logging.Logger))
        self.assertEqual(logger.logging_provider, 'logstash')

        temlogger.config.set_provider('default')
        logger = temlogger.getLogger('switch-logger-1')
        self.assertTrue(isinstance(logger, logging.Logger))
        self.assertEqual(logger.logging_provider, 'default')

    def test_get_logstash_logger_passing_envs_by_environ(self):
        os.environ['TEMLOGGER_PROVIDER'] = 'logstash'
        os.environ['TEMLOGGER_URL'] = 'localhost'
        os.environ['TEMLOGGER_PORT'] = '5000'

        logger = temlogger.getLogger('logstash-2')
        self.assertEqual(logger.logging_provider, 'logstash')

    def test_get_logstash_logger_passing_envs_as_parameter(self):
        temlogger.config.set_provider('logstash')
        temlogger.config.set_url('localhost')
        temlogger.config.set_port('5000')
        temlogger.config.set_environment('staging')

        logger = temlogger.getLogger('logstash-3')
        self.assertEqual(logger.logging_provider, 'logstash')

    def test_get_logstash_logger_and_log_info(self):
        """"""
        temlogger.config.set_provider('logstash')
        temlogger.config.set_url('localhost')
        temlogger.config.set_port('5000')

        logger = temlogger.getLogger('logstash-3')

        self.assertEqual(len(logger.handlers), 1)
        self.assertEqual(logger.logging_provider, 'logstash')

        logger._log = mock.Mock()

        logger.info('Logstash log')

        logger._log.assert_called_once_with(logging.INFO, 'Logstash log', ())


class TestStackDriverLogger(unittest.TestCase):
    """
    Based on official tests:
    https://github.com/googleapis/google-cloud-python/blob/master/logging/tests/unit/test_logger.py
    """

    def setUp(self):
        """
        Clean config between tests
        """
        clean_temlogger_config()

    @mock.patch("google.cloud.logging.Client")
    def test_get_stackdriver_logger_passing_envs_by_environ(self, mocked_cls):
        os.environ['TEMLOGGER_PROVIDER'] = 'stackdriver'

        logger = temlogger.getLogger('stackdriver-1')

        self.assertTrue(isinstance(logger, logging.Logger))
        self.assertEqual(logger.logging_provider, 'stackdriver')

    @mock.patch("google.cloud.logging.Client")
    def test_get_stackdriver_logger_passing_envs_as_parameter(self, mocked_cls):
        """"""
        temlogger.config.set_provider('stackdriver')

        logger = temlogger.getLogger('stackdriver-2')
        self.assertEqual(logger.logging_provider, 'stackdriver')

    @mock.patch("google.cloud.logging.Client")
    def test_get_stackdriver_logger_and_log_info(self, mocked_cls):
        """"""
        temlogger.config.set_provider('stackdriver')

        logger = temlogger.getLogger('stackdriver-2')

        self.assertEqual(len(logger.handlers), 1)
        self.assertEqual(logger.logging_provider, 'stackdriver')

        logger._log = mock.Mock()

        logger.info('StackDriver log')

        logger._log.assert_called_once_with(
            logging.INFO, 'StackDriver log', ())

    def test_stackdriver_with_credentials_base64(self):
        valid_cred = encode_file_as_base64(VALID_GOOGLE_CREDENTIALS)

        temlogger.config.set_provider('stackdriver')
        temlogger.config.set_google_credentials_base64(valid_cred)
        temlogger.getLogger('stackdriver-base64')

    def test_stackdriver_with_credentials_base64_as_environment(self):
        valid_cred = encode_file_as_base64(VALID_GOOGLE_CREDENTIALS)

        os.environ['TEMLOGGER_GOOGLE_CREDENTIALS_BASE64'] = valid_cred

        temlogger.config.set_provider('stackdriver')
        temlogger.getLogger('stackdriver-base64')


class TestConsoleLogger(unittest.TestCase):

    def setUp(self):
        """
        Clean config between tests
        """
        clean_temlogger_config()

    def test_get_console_logger_passing_envs_by_environ(self):
        os.environ['TEMLOGGER_PROVIDER'] = 'console'

        logger = temlogger.getLogger('console-logger-1')

        self.assertTrue(isinstance(logger, logging.Logger))
        self.assertEqual(logger.logging_provider, 'console')

    def test_get_console_logger_passing_envs_as_parameter(self):
        temlogger.config.set_provider('console')

        logger = temlogger.getLogger('console-logger-2')
        self.assertEqual(logger.logging_provider, 'console')

    def test_get_console_logger_and_assert_log_was_sent_out(self):
        import sys
        temlogger.config.set_provider('console')

        logger = temlogger.getLogger('console-3')

        self.assertEqual(len(logger.handlers), 1)
        self.assertEqual(logger.logging_provider, 'console')

        log_message = 'Console log entry message'
        log_record = logging.makeLogRecord({'msg': log_message})

        handler = logger.handlers[0]

        handler.emit = mock.Mock()

        logger.info(log_message)

        # handler.emit calls handler.stream(sys.stderror.write) to write logs
        assert handler.stream == sys.stderr
        handler.emit.assert_called_once()
        self.assertTrue(log_message in str(handler.emit.call_args_list))
