import unittest

from ..helpers import import_string
from ..helpers import import_string_list
from ..temlogger import config


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
