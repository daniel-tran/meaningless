import unittest
import sys
sys.path.append('../')
from meaningless import XMLExtractor, xml_file_interface

# These tests just test for certain components which differ from the base extractor


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def test_xml_extractor_settings(self):
        bible = XMLExtractor()
        self.assertEqual(bible.file_extension, '.xml', 'Extension is incorrect')
        self.assertEqual(bible.file_reading_function.__module__, xml_file_interface.read.__module__,
                         'Module of reading function is incorrect')
        self.assertEqual(bible.file_reading_function.__name__, xml_file_interface.read.__name__,
                         'Name of reading function is incorrect')
        self.assertTrue(bible.read_key_as_string, 'Extractor is not reading keys as strings')


if __name__ == "__main__":
    unittest.main()
