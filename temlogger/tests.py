import logging
import os
import unittest
import temlogger
from unittest import mock


class GetLoggerTestCase(unittest.TestCase):

    def tearDown(self):
        """
        Clean config between tests
        """
        environments_to_clean = [
            'LOGGING_PROVIDER',
            'LOGGING_URL',
            'LOGGING_PORT'
        ]
        for env in environments_to_clean:
            if env in os.environ:
                del os.environ[env]

        temlogger.config.set_logging_provider('')
        temlogger.config.set_logging_url('')
        temlogger.config.set_logging_port('')

    def test_getlogger_without_set_logging_provider_return_none(self):
        logger = temlogger.getLogger('test')

        self.assertTrue(isinstance(logger, logging.Logger))

    def test_can_getlogger_logstash(self):
        logger = temlogger.getLogger('logstash-1')
        logger.logging_provider = 'logstash'
        logger.logstash_url = 'localhost'
        logger.logstash_port = 5000

    def test_get_logstash_logger_passing_logstash_envs(self):
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

    def test_get_stackdriver_logger_passing_envs_as_parameter(self):
        temlogger.config.set_logging_provider('stackdriver')
        temlogger.config.set_logging_url('localhost')
        temlogger.config.set_logging_port('5000')

        logger = temlogger.getLogger('stackdriver-1')
        self.assertEqual(logger.logging_provider, 'stackdriver')
