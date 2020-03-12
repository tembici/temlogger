import os
import socket
import temlogger
import unittest
import logging
import uuid

from unittest.mock import patch

from .base import clean_temlogger_config
from temlogger.providers.base import FormatterBase


class TestEventHandler(unittest.TestCase):

    def setUp(self):
        """
        Clean config between tests
        """
        clean_temlogger_config()

    @patch.object(FormatterBase, 'format_timestamp',
                  lambda *_: '2020-03-06T21:29:36.246Z')
    def test_register_one_handler_global(self):

        def add_tracker_id(message):
            message['tracker_id'] = 'tracker_id_hex'
            return message

        temlogger.config.set_provider('logstash')
        temlogger.config.setup_event_handlers([add_tracker_id])

        logger = temlogger.getLogger('first_handler')

        format_base = FormatterBase()
        with patch.object(FormatterBase, 'format_with_handlers',
                          wraps=format_base.format_with_handlers) as mock_fwh:

            logger_message = 'First handler message'
            logger.info(logger_message)

            expected = {
                '@timestamp': '2020-03-06T21:29:36.246Z',
                'message': logger_message,
                'host': socket.gethostname(),
                'path': os.path.abspath(__file__),
                'tracker_id': 'tracker_id_hex',
                'environment': '', 'level': 'INFO',
                'logger_name': logger.name,
                'stack_info': None
            }
            mock_fwh.assert_called_once_with(expected)

    def test_register_handler_twice(self):

        def add_tracker_id(message):
            message['tracker_id'] = 'tracker_id_hex'
            return message

        temlogger.config.set_provider('logstash')
        temlogger.config.setup_event_handlers([add_tracker_id])

        self.assertIn(add_tracker_id, temlogger.config.get_event_handlers())
        self.assertEqual(1, len(temlogger.config.get_event_handlers()))

        temlogger.config.setup_event_handlers([lambda x: x])

        self.assertNotIn(add_tracker_id, temlogger.config.get_event_handlers())
        self.assertEqual(1, len(temlogger.config.get_event_handlers()))

    @patch.object(FormatterBase, 'format_timestamp',
                  lambda *_: '2020-03-06T21:29:36.246Z')
    def test_register_two_handler_global(self):
        def tracker_id_param(message):
            message['tracker_id'] = 'tracker_id_hex'
            return message

        def add_request_id_param(message):
            message['request_id'] = 'request_id_hex2'
            return message

        temlogger.config.set_provider('logstash')
        temlogger.config.setup_event_handlers([
            tracker_id_param,
            add_request_id_param
        ])

        logger = temlogger.getLogger('two_handler')

        formatter = logger.handlers[0].formatter
        with patch.object(FormatterBase, 'format_with_handlers',
                          wraps=formatter.format_with_handlers) as mock_fwh:

            logger_message = 'Two handler message'
            logger.info(logger_message)

            expected = {
                '@timestamp': '2020-03-06T21:29:36.246Z',
                'message': logger_message,
                'host': socket.gethostname(),
                'path': os.path.abspath(__file__),
                'tracker_id': 'tracker_id_hex',
                'request_id': 'request_id_hex2',
                'environment': '', 'level': 'INFO',
                'logger_name': logger.name,
                'stack_info': None
            }
            mock_fwh.assert_called_once_with(expected)

    def test_register_event_handler_that_clear_message_keys(self):
        def clear_keys(message):
            message.clear()
            return message

        temlogger.config.set_provider('logstash')
        temlogger.config.setup_event_handlers([clear_keys])

        logger = temlogger.getLogger('three_handler')

        formatter = logger.handlers[0].formatter

        with patch.object(FormatterBase, 'format_with_handlers',
                          wraps=formatter.format_with_handlers) as mock_fwh:
            logger.info('Two handler')

            expected = {}
            mock_fwh.assert_called_once_with(expected)

    @patch.object(FormatterBase, 'format_timestamp',
                  lambda *_: '2020-03-06T21:29:36.246Z')
    def test_register_dotted_string_module(self):
        def clear_keys(message):
            message.clear()
            return message

        temlogger.config.set_provider('logstash')
        temlogger.config.setup_event_handlers([
            'temlogger.tests.base.add_tracker_id_to_message',
        ])

        logger = temlogger.getLogger('four_handler')

        formatter = logger.handlers[0].formatter

        with patch.object(FormatterBase, 'format_with_handlers',
                          wraps=formatter.format_with_handlers) as mock_fwh:

            logger_message = 'Four handler message'
            logger.info(logger_message)

            expected = {
                '@timestamp': '2020-03-06T21:29:36.246Z',
                'message': logger_message,
                'host': socket.gethostname(),
                'path': os.path.abspath(__file__),
                'environment': '', 'level': 'INFO',
                'logger_name': logger.name,
                'stack_info': None,
                'tracker_id_global': 'tracker_id_value_global',
            }
            mock_fwh.assert_called_once_with(expected)

    @patch.object(FormatterBase, 'format_timestamp',
                  lambda *_: '2020-03-06T21:29:36.246Z')
    def test_register_dotted_string_module_and_function(self):
        random_key = uuid.uuid4().hex

        def add_random_key_to_message(message):
            message['random_key'] = random_key
            return message

        temlogger.config.set_provider('logstash')
        temlogger.config.setup_event_handlers([
            'temlogger.tests.base.add_tracker_id_to_message',
            add_random_key_to_message,
        ])

        logger = temlogger.getLogger('four_handler')

        formatter = logger.handlers[0].formatter

        with patch.object(FormatterBase, 'format_with_handlers',
                          wraps=formatter.format_with_handlers) as mock_fwh:

            logger_message = 'Four handler message'
            logger.info(logger_message)

            expected = {
                '@timestamp': '2020-03-06T21:29:36.246Z',
                'message': logger_message,
                'host': socket.gethostname(),
                'path': os.path.abspath(__file__),
                'environment': '', 'level': 'INFO',
                'logger_name': logger.name,
                'stack_info': None,
                'tracker_id_global': 'tracker_id_value_global',
                'random_key': random_key,
            }
            mock_fwh.assert_called_once_with(expected)

    @patch.object(FormatterBase, 'format_timestamp',
                  lambda *_: '2020-03-06T21:29:36.246Z')
    def test_register_event_handler_on_one_logger_only(self):
        random_key = uuid.uuid4().hex

        def add_random_key_to_message_local(message):
            message['random_key'] = random_key
            return message

        temlogger.config.set_provider('logstash')
        logger = temlogger.getLogger('five_handler', event_handlers=[
            add_random_key_to_message_local
        ])

        handler = logger.handlers[0]
        formatter = handler.formatter

        with patch.object(FormatterBase, 'format_with_handlers',
                          wraps=formatter.format_with_handlers) as mock_fwh:

            logger_message = 'Five handler message'
            logger.info(logger_message)

            expected = {
                '@timestamp': '2020-03-06T21:29:36.246Z',
                'message': logger_message,
                'host': socket.gethostname(),
                'path': os.path.abspath(__file__),
                'environment': '',
                'level': 'INFO',
                'logger_name': logger.name,
                'stack_info': None,
                'random_key': random_key,
            }
            mock_fwh.assert_called_once_with(expected)
