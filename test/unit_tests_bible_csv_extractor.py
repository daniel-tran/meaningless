import unittest
import sys
sys.path.append('../')
from meaningless import CSVExtractor, csv_file_interface

# These tests just test for certain components which differ from the base extractor


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def test_json_extractor_settings(self):
        bible = CSVExtractor()
        self.assertEqual(bible.file_extension, '.csv', 'Extension is incorrect')
        self.assertEqual(bible.file_reading_function.__module__, csv_file_interface.read.__module__,
                         'Module of reading function is incorrect')
        self.assertEqual(bible.file_reading_function.__name__, csv_file_interface.read.__name__,
                         'Name of reading function is incorrect')
        self.assertTrue(bible.read_key_as_string, 'Extractor is not reading keys as strings')


if __name__ == "__main__":
    unittest.main()
