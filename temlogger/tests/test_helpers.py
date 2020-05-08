import unittest

from ..helpers import import_string
from ..helpers import import_string_list
from ..helpers import load_google_client
from ..helpers import encode_file_as_base64
from ..temlogger import config
from .base import VALID_GOOGLE_CREDENTIALS
from .base import INVALID_GOOGLE_CREDENTIALS


class TestImportString(unittest.TestCase):

    def test_import_raise_attribute_error(self):

        with self.assertRaises(ImportError) as ctx:
            import_string('temlogger.no_existing_module')

        self.assertIsInstance(ctx.exception, ImportError)

    def test_import_raise_value_error(self):

        with self.assertRaises(ImportError) as ctx:
            import_string('any_module')

        self.assertIsInstance(ctx.exception, ImportError)


class TestImportStringList(unittest.TestCase):

    def test_import_string_list_zero_modules(self):

        modules = import_string_list([])

        self.assertEqual(len(modules), 0)

    def test_import_string_list__one_module(self):

        modules = import_string_list(
            ['temlogger.config']
        )

        self.assertEqual(len(modules), 1)
        self.assertEqual(type(config), type(modules[0]))

    def test_import_string_list_mixed_modules(self):
        def one_more_func():
            pass

        modules = import_string_list([
            'temlogger.config',
            lambda x: x,
            one_more_func,
        ])

        self.assertEqual(len(modules), 3)
        self.assertEqual(type(config), type(modules[0]))
        self.assertEqual(type(one_more_func), type(one_more_func))


class TestLoadGoogleClient(unittest.TestCase):

    def setUp(self):
        self.invalid_cred_base64 = encode_file_as_base64(
            INVALID_GOOGLE_CREDENTIALS)
        self.valid_cred_base64 = encode_file_as_base64(
            VALID_GOOGLE_CREDENTIALS)

    def test_load_google_client_with_empty_string(self):

        cred = load_google_client('')

        self.assertEqual(cred, '')

    def test_load_google_client_with_invalid_credential(self):
        """
        raise ValueError: ValueError: Service account info was not in the
        expected format, missing fields token_uri.

        """
        with self.assertRaises(ValueError) as raized_exception:
            load_google_client(self.invalid_cred_base64)

            self.assertEqual(raized_exception, ValueError)

    def test_load_google_client_with_valid_credential(self):
        from google.cloud.logging import Client

        cred = load_google_client(self.valid_cred_base64)

        self.assertIsInstance(cred, Client)
