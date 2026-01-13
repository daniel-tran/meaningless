import unittest
import sys
sys.path.append('../')
from meaningless import TOMLExtractor, toml_file_interface

# These tests just test for certain components which differ from the base extractor


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def test_toml_extractor_settings(self):
        bible = TOMLExtractor()
        self.assertEqual(bible.file_extension, '.toml', 'Extension is incorrect')
        self.assertEqual(bible.file_reading_function.__module__, toml_file_interface.read.__module__,
                         'Module of reading function is incorrect')
        self.assertEqual(bible.file_reading_function.__name__, toml_file_interface.read.__name__,
                         'Name of reading function is incorrect')
        self.assertTrue(bible.read_key_as_string, 'Extractor is not reading keys as strings')


if __name__ == "__main__":
    unittest.main()