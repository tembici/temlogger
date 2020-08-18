import os
import logging
import unittest

from ..helpers import encode_file_as_base64
from ..helpers import import_string
from ..helpers import import_string_list
from ..helpers import load_google_client
from ..temlogger import config
from .base import INVALID_GOOGLE_CREDENTIALS
from .base import VALID_GOOGLE_CREDENTIALS
from .base import clean_temlogger_config


class TestLoggingConfig(unittest.TestCase):

    def setUp(self):
        """
        Clean config between tests
        """
        clean_temlogger_config()

    def test_set_provider_and_get_provider(self):

        self.assertEqual(config.get_provider(), 'default')
        config.set_provider('console')
        self.assertEqual(config.get_provider(), 'console')

    def test_set_log_level_and_get_log_level(self):

        self.assertEqual(config.get_log_level(), 'INFO')
        self.assertEqual(config.get_log_level_parsed(), logging.INFO)

        config.set_log_level('DEBUG')

        self.assertEqual(config.get_log_level(), 'DEBUG')
        self.assertEqual(config.get_log_level_parsed(), logging.DEBUG)

    def test_inexistent_log_level_try_set_log_level_and_get_log_level(self):

        self.assertEqual(config.get_log_level(), 'INFO')
        self.assertEqual(config.get_log_level_parsed(), logging.INFO)

        config.set_log_level('INEXISTENT')

        self.assertEqual(config.get_log_level(), 'INEXISTENT')
        # More information about python logging see:
        # https://bugs.python.org/issue22386
        self.assertEqual(config.get_log_level_parsed(), 'Level INEXISTENT')

    def test_environment_variable_try_set_log_level_and_get_log_level(self):

        self.assertEqual(config.get_log_level(), 'INFO')
        self.assertEqual(config.get_log_level_parsed(), logging.INFO)

        os.environ['TEMLOGGER_LOG_LEVEL'] = 'DEBUG'

        self.assertEqual(config.get_log_level(), 'DEBUG')
        self.assertEqual(config.get_log_level_parsed(), logging.DEBUG)
