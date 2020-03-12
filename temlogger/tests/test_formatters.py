import json
import unittest
import logging

from .base import clean_temlogger_config
from ..providers.default import DefaultFormatter
from ..providers.logstash import LogstashFormatter
from ..providers.stackdriver import StackDriverFormatter


class TestDefaultFormatter(unittest.TestCase):

    def setUp(self):
        """
        Clean config between tests
        """
        clean_temlogger_config()

    def test_format(self):

        formater = DefaultFormatter(environment='develop')
        log_message = 'Log entry message'

        record = logging.makeLogRecord({'msg': log_message})

        str_message = formater.format(record)
        self.assertIsInstance(str_message, str)

        message = json.loads(str_message)

        self.assertEqual(message['message'], log_message)
        self.assertEqual(message['environment'], 'develop')


class TestLogstashFormatter(unittest.TestCase):

    def setUp(self):
        """
        Clean config between tests
        """
        clean_temlogger_config()

    def test_format(self):

        formater = LogstashFormatter(environment='develop')
        log_message = 'Log entry message'

        record = logging.makeLogRecord({'msg': log_message})

        str_message = formater.format(record)
        message = json.loads(str_message)

        self.assertIsInstance(str_message, str)
        self.assertEqual(message['message'], log_message)
        self.assertEqual(message['environment'], 'develop')


class TestStackDriverFormatter(unittest.TestCase):

    def setUp(self):
        """
        Clean config between tests
        """
        clean_temlogger_config()

    def test_format(self):

        formater = StackDriverFormatter(environment='develop')
        log_message = 'Log entry message'

        record = logging.makeLogRecord({'msg': log_message})

        message = formater.format(record)

        self.assertEqual(message['message'], log_message)
        self.assertEqual(message['environment'], 'develop')
