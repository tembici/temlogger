import json
import unittest
import logging

from .base import clean_temlogger_config
from ..providers.default import DefaultFormatter
from ..providers.logstash import LogstashFormatter
from ..providers.stackdriver import StackDriverFormatter
from ..providers.console import ConsoleFormatter


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

        self.assertTrue('payload' in message)
        self.assertEqual(message['message'], log_message)
        self.assertEqual(message['environment'], 'develop')

    def test_format_with_extra(self):
        formater = DefaultFormatter(environment='develop')
        log_message = 'Log entry message'

        record = logging.makeLogRecord({
            'msg': log_message, 'extra_field': 'Extra Field'}
        )

        str_message = formater.format(record)
        message = json.loads(str_message)
        payload = message['payload']

        self.assertTrue('payload' in message)
        self.assertEqual(payload['extra_field'], 'Extra Field')
        self.assertEqual(message['message'], log_message)
        self.assertEqual(message['environment'], 'develop')

    def test_format_with_app_name_and_extra(self):
        formater = StackDriverFormatter(
            app_name='stackdriver-app', environment='develop'
        )
        log_message = 'Log entry message'

        record = logging.makeLogRecord({
            'msg': log_message, 'extra_field': 'Extra Field'}
        )

        message = formater.format(record)
        payload = message['payload']

        self.assertTrue('payload' in message)
        self.assertEqual(payload['extra_field'], 'Extra Field')
        self.assertEqual(message['message'], log_message)
        self.assertEqual(message['environment'], 'develop')
        self.assertEqual(message['app_name'], 'stackdriver-app')


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
        self.assertTrue('payload' in message)
        self.assertEqual(message['message'], log_message)
        self.assertEqual(message['environment'], 'develop')

    def test_format_with_extra(self):
        formater = LogstashFormatter(environment='develop')
        log_message = 'Log entry message'

        record = logging.makeLogRecord({
            'msg': log_message, 'extra_field': 'Extra Field'}
        )

        str_message = formater.format(record)
        message = json.loads(str_message)
        payload = message['payload']

        self.assertTrue('payload' in message)
        self.assertEqual(payload['extra_field'], 'Extra Field')
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

        self.assertTrue('payload' in message)
        self.assertEqual(message['message'], log_message)
        self.assertEqual(message['environment'], 'develop')

    def test_format_with_extra(self):
        formater = StackDriverFormatter(environment='develop')
        log_message = 'Log entry message'

        record = logging.makeLogRecord({
            'msg': log_message, 'extra_field': 'Extra Field'}
        )

        message = formater.format(record)
        payload = message['payload']

        self.assertTrue('payload' in message)
        self.assertEqual(payload['extra_field'], 'Extra Field')
        self.assertEqual(message['message'], log_message)
        self.assertEqual(message['environment'], 'develop')

class TestConsoleFormatter(unittest.TestCase):

    def setUp(self):
        """
        Clean config between tests
        """
        clean_temlogger_config()

    def test_format(self):
        formater = ConsoleFormatter(environment='develop')
        log_message = 'Log entry message'

        record = logging.makeLogRecord({'msg': log_message})

        str_message = formater.format(record)
        message = json.loads(str_message)

        self.assertTrue('payload' in message)
        self.assertEqual(message['message'], log_message)
        self.assertEqual(message['environment'], 'develop')

    def test_format_with_extra(self):
        formater = ConsoleFormatter(environment='develop')
        log_message = 'Log entry message'

        record = logging.makeLogRecord({
            'msg': log_message, 'extra_field': 'Extra Field'}
        )

        str_message = formater.format(record)
        message = json.loads(str_message)
        payload = message['payload']

        self.assertTrue('payload' in message)
        self.assertEqual(payload['extra_field'], 'Extra Field')
        self.assertEqual(message['message'], log_message)
        self.assertEqual(message['environment'], 'develop')
