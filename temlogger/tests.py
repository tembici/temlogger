import logging
import os
import unittest
import temlogger
from unittest import mock


def clean_temlogger_config():
    environments_to_clean = [
        'LOGGING_PROVIDER',
        'LOGGING_URL',
        'LOGGING_PORT'
    ]
    for env in environments_to_clean:
        if env in os.environ:
            del os.environ[env]

    temlogger.config.clear()


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

        temlogger.config.set_logging_provider('logstash')
        logger = temlogger.getLogger('switch-logger-1')
        self.assertTrue(isinstance(logger, logging.Logger))
        self.assertEqual(logger.logging_provider, 'logstash')

        temlogger.config.set_logging_provider('default')
        logger = temlogger.getLogger('switch-logger-1')
        self.assertTrue(isinstance(logger, logging.Logger))
        self.assertEqual(logger.logging_provider, 'default')

    def test_get_logstash_logger_passing_envs_by_environ(self):
        os.environ['LOGGING_PROVIDER'] = 'logstash'
        os.environ['LOGGING_URL'] = 'localhost'
        os.environ['LOGGING_PORT'] = '5000'

        logger = temlogger.getLogger('logstash-2')
        self.assertEqual(logger.logging_provider, 'logstash')

    def test_get_logstash_logger_passing_envs_as_parameter(self):
        temlogger.config.set_logging_provider('logstash')
        temlogger.config.set_logging_url('localhost')
        temlogger.config.set_logging_port('5000')

        logger = temlogger.getLogger('logstash-3')
        self.assertEqual(logger.logging_provider, 'logstash')

    def test_get_logstash_logger_and_log_info(self):
        """"""
        temlogger.config.set_logging_provider('logstash')
        temlogger.config.set_logging_url('localhost')
        temlogger.config.set_logging_port('5000')

        logger = temlogger.getLogger('logstash-3')

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
        os.environ['LOGGING_PROVIDER'] = 'stackdriver'

        logger = temlogger.getLogger('stackdriver-1')

        self.assertTrue(isinstance(logger, logging.Logger))
        self.assertEqual(logger.logging_provider, 'stackdriver')

    @mock.patch("google.cloud.logging.Client")
    def test_get_stackdriver_logger_passing_envs_as_parameter(self, mocked_cls):
        """"""
        temlogger.config.set_logging_provider('stackdriver')

        logger = temlogger.getLogger('stackdriver-2')
        self.assertEqual(logger.logging_provider, 'stackdriver')

    @mock.patch("google.cloud.logging.Client")
    def test_get_stackdriver_logger_and_log_info(self, mocked_cls):
        """"""
        temlogger.config.set_logging_provider('stackdriver')

        logger = temlogger.getLogger('stackdriver-2')

        self.assertEqual(logger.logging_provider, 'stackdriver')

        logger._log = mock.Mock()

        logger.info('StackDriver log')

        logger._log.assert_called_once_with(logging.INFO, 'StackDriver log', ())
