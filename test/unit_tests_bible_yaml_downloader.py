import unittest
import sys
import os
import filecmp
sys.path.append('../src/')
from meaningless import bible_yaml_downloader


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def test_yaml_download(self):
        bible_yaml_downloader.yaml_download('Philemon', file_location='./tmp/test_yaml_download/')
        self.assertTrue(filecmp.cmp('./tmp/test_yaml_download/NIV/Philemon.yaml',
                                    './static/NIV/test_yaml_download.yaml'),
                        'Files do not match')

    def test_yaml_download_without_passage_numbers(self):
        bible_yaml_downloader.yaml_download('Philemon',
                                            file_location='./tmp/test_yaml_download_without_passage_numbers/',
                                            show_passage_numbers=False)
        self.assertTrue(filecmp.cmp('./tmp/test_yaml_download_without_passage_numbers/NIV/Philemon.yaml',
                                    './static/NIV/test_yaml_download_without_passage_numbers.yaml'),
                        'Files do not match')

    def test_yaml_download_invalid_book(self):
        bible_yaml_downloader.yaml_download('Barnabas', file_location='./tmp/test_yaml_download_invalid_book/')
        # An invalid book should fail fast and not bother with downloading
        self.assertFalse(os.path.exists('./tmp/test_yaml_download_invalid_book/'), 'File should not have downloaded')

if __name__ == "__main__":
    unittest.main()
