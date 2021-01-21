import unittest
import sys
sys.path.append('../')
from meaningless import JSONDownloader, json_file_interface

# These tests just test for certain components which differ from the base downloader


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def test_json_downloader_settings(self):
        bible = JSONDownloader()
        self.assertEqual(bible.file_extension, '.json', 'Extension is incorrect')
        self.assertEqual(bible.file_writing_function.__module__, json_file_interface.write.__module__,
                         'Module of writing function is incorrect')
        self.assertEqual(bible.file_writing_function.__name__, json_file_interface.write.__name__,
                         'Name of writing function is incorrect')

if __name__ == "__main__":
    unittest.main()
