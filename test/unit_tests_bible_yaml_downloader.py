import unittest
import sys
import os
import filecmp
sys.path.append('../src/')
from meaningless.bible_yaml_downloader import YAMLDownloader
from meaningless.utilities import yaml_file_interface


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def test_yaml_download(self):
        download_path = './tmp/test_yaml_download'
        bible = YAMLDownloader(file_location=download_path)
        bible.download_book('Philemon')
        self.assertTrue(filecmp.cmp('{0}/NIV/Philemon.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download.yaml'),
                        'Files do not match')

    def test_yaml_download_without_passage_numbers(self):
        download_path = './tmp/test_yaml_download_without_passage_numbers'
        bible = YAMLDownloader(file_location=download_path, show_passage_numbers=False)
        bible.download_book('Philemon')
        self.assertTrue(filecmp.cmp('{0}/NIV/Philemon.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download_without_passage_numbers.yaml'),
                        'Files do not match')

    def test_yaml_download_invalid_book(self):
        download_path = './tmp/test_yaml_download_invalid_book'
        bible = YAMLDownloader(file_location=download_path)
        bible.download_book('Barnabas')
        # An invalid book should fail fast and not bother with downloading
        self.assertFalse(os.path.exists(download_path), 'File should not have downloaded')

    def test_yaml_download_nlt(self):
        download_path = './tmp/test_yaml_download_nlt'
        bible = YAMLDownloader(file_location=download_path, translation='NLT')
        bible.download_book('Philemon')
        self.assertTrue(filecmp.cmp('{0}/NLT/Philemon.yaml'.format(download_path),
                                    './static/NLT/test_yaml_download_nlt.yaml'),
                        'Files do not match')

    def test_yaml_download_omitted_passage(self):
        download_path = './tmp/test_yaml_download_omitted_passage'
        bible = YAMLDownloader(file_location=download_path, translation='NLT')
        bible.download_book('Romans')
        text = yaml_file_interface.read('{0}/NLT/Romans.yaml'.format(download_path))['Romans'][16][24]
        self.assertEqual('', text, 'Files do not match')

    def test_yaml_download_with_stripped_whitespaces(self):
        download_path = './tmp/test_yaml_download_with_stripped_whitespaces'
        bible = YAMLDownloader(file_location=download_path, strip_excess_whitespace=True)
        bible.download_book('Philemon')
        self.assertTrue(filecmp.cmp('{0}/NIV/Philemon.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download_with_stripped_whitespaces.yaml'),
                        'Files do not match')

    def test_yaml_download_passage(self):
        download_path = './tmp/test_yaml_download_passage'
        bible = YAMLDownloader(file_location=download_path)
        bible.download_passage('Philemon', 1, 1)
        self.assertTrue(filecmp.cmp('{0}/NIV/Philemon.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download_passage.yaml'),
                        'Files do not match')

    def test_yaml_download_passages(self):
        download_path = './tmp/test_yaml_download_passages'
        bible = YAMLDownloader(file_location=download_path)
        bible.download_passages('Philemon', 1, 1, 3)
        self.assertTrue(filecmp.cmp('{0}/NIV/Philemon.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download_passages.yaml'),
                        'Files do not match')

    def test_yaml_download_chapter(self):
        download_path = './tmp/test_yaml_download_chapter'
        bible = YAMLDownloader(file_location=download_path)
        bible.download_chapter('1 John', 1)
        self.assertTrue(filecmp.cmp('{0}/NIV/1 John.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download_chapter.yaml'),
                        'Files do not match')

    def test_yaml_download_chapters(self):
        download_path = './tmp/test_yaml_download_chapter'
        bible = YAMLDownloader(file_location=download_path)
        bible.download_chapters('1 John', 1, 3)
        self.assertTrue(filecmp.cmp('{0}/NIV/1 John.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download_chapters.yaml'),
                        'Files do not match')

    def test_yaml_download_passage_range(self):
        download_path = './tmp/test_yaml_download_passage_range'
        bible = YAMLDownloader(file_location=download_path)
        bible.download_passage_range('1 John', 1, 3, 1, 5)
        self.assertTrue(filecmp.cmp('{0}/NIV/1 John.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download_passage_range.yaml'),
                        'Files do not match')

    def test_yaml_download_with_misc_info(self):
        download_path = './tmp/test_yaml_download_with_misc_info'
        bible = YAMLDownloader(file_location=download_path, include_misc_info=True)
        bible.download_book('Philemon')
        document = yaml_file_interface.read('{0}/NIV/Philemon.yaml'.format(download_path))
        # For some reason, the misc. info is always placed after the passage contents in these tests?
        self.assertEqual('English', document['Info']['Language'], 'Language info is not correct')
        self.assertEqual('NIV', document['Info']['Translation'], 'Translation info is not correct')

if __name__ == "__main__":
    unittest.main()
