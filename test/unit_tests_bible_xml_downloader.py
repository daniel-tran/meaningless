import unittest
import sys
sys.path.append('../')
from meaningless import XMLDownloader, xml_file_interface

# These tests just test for certain components which differ from the base downloader


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def test_xml_downloader_settings(self):
        bible = XMLDownloader()
        self.assertEqual(bible.file_extension, '.xml', 'Extension is incorrect')
        self.assertEqual(bible.file_writing_function.__module__, xml_file_interface.write.__module__,
                         'Module of writing function is incorrect')
        self.assertEqual(bible.file_writing_function.__name__, xml_file_interface.write.__name__,
                         'Name of writing function is incorrect')
        self.assertTrue(bible.write_key_as_string, 'Downloader is not writing keys as strings')


if __name__ == "__main__":
    unittest.main()
