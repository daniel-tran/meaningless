import unittest
import sys
import os
import filecmp
sys.path.append('../src/')
from meaningless.bible_yaml_downloader import YAMLDownloader
from meaningless.utilities import yaml_file_interface
from meaningless.utilities.exceptions import InvalidSearchError, InvalidPassageError


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def test_yaml_download(self):
        download_path = './tmp/test_yaml_download/NIV'
        bible = YAMLDownloader(default_directory=download_path)
        bible.download_book('Philemon')
        self.assertTrue(filecmp.cmp('{0}/Philemon.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download.yaml'),
                        'Files do not match')

    def test_yaml_download_without_passage_numbers(self):
        download_path = './tmp/test_yaml_download_without_passage_numbers/NIV'
        bible = YAMLDownloader(default_directory=download_path, show_passage_numbers=False)
        bible.download_book('Philemon')
        self.assertTrue(filecmp.cmp('{0}/Philemon.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download_without_passage_numbers.yaml'),
                        'Files do not match')

    def test_yaml_download_invalid_book(self):
        download_path = './tmp/test_yaml_download_invalid_book/NIV'
        bible = YAMLDownloader(default_directory=download_path)
        # An invalid book should fail fast and not bother with downloading
        self.assertRaises(InvalidPassageError, bible.download_book, 'Barnabas')

    def test_yaml_download_nlt(self):
        download_path = './tmp/test_yaml_download_nlt/NLT'
        bible = YAMLDownloader(default_directory=download_path, translation='NLT')
        bible.download_book('Philemon')
        self.assertTrue(filecmp.cmp('{0}/Philemon.yaml'.format(download_path),
                                    './static/NLT/test_yaml_download_nlt.yaml'),
                        'Files do not match')

    def test_yaml_download_omitted_passage(self):
        download_path = './tmp/test_yaml_download_omitted_passage/NLT'
        bible = YAMLDownloader(default_directory=download_path, translation='NLT')
        bible.download_book('Romans')
        text = yaml_file_interface.read('{0}/Romans.yaml'.format(download_path))['Romans'][16][24]
        self.assertEqual('', text, 'Files do not match')

    def test_yaml_download_with_stripped_whitespaces(self):
        download_path = './tmp/test_yaml_download_with_stripped_whitespaces/NIV'
        bible = YAMLDownloader(default_directory=download_path, strip_excess_whitespace=True)
        bible.download_book('Philemon')
        self.assertTrue(filecmp.cmp('{0}/Philemon.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download_with_stripped_whitespaces.yaml'),
                        'Files do not match')

    def test_yaml_download_passage(self):
        download_path = './tmp/test_yaml_download_passage/NIV'
        bible = YAMLDownloader(default_directory=download_path)
        bible.download_passage('Philemon', 1, 1)
        self.assertTrue(filecmp.cmp('{0}/Philemon.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download_passage.yaml'),
                        'Files do not match')

    def test_yaml_download_passages(self):
        download_path = './tmp/test_yaml_download_passages/NIV'
        bible = YAMLDownloader(default_directory=download_path)
        bible.download_passages('Philemon', 1, 1, 3)
        self.assertTrue(filecmp.cmp('{0}/Philemon.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download_passages.yaml'),
                        'Files do not match')

    def test_yaml_download_chapter(self):
        download_path = './tmp/test_yaml_download_chapter/NIV'
        bible = YAMLDownloader(default_directory=download_path)
        bible.download_chapter('1 John', 1)
        self.assertTrue(filecmp.cmp('{0}/1 John.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download_chapter.yaml'),
                        'Files do not match')

    def test_yaml_download_chapters(self):
        download_path = './tmp/test_yaml_download_chapter/NIV'
        bible = YAMLDownloader(default_directory=download_path)
        bible.download_chapters('1 John', 1, 3)
        self.assertTrue(filecmp.cmp('{0}/1 John.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download_chapters.yaml'),
                        'Files do not match')

    def test_yaml_download_passage_range(self):
        download_path = './tmp/test_yaml_download_passage_range/NIV'
        bible = YAMLDownloader(default_directory=download_path)
        bible.download_passage_range('1 John', 1, 3, 1, 5)
        self.assertTrue(filecmp.cmp('{0}/1 John.yaml'.format(download_path),
                                    './static/NIV/test_yaml_download_passage_range.yaml'),
                        'Files do not match')

    def test_yaml_download_with_misc_info(self):
        download_path = './tmp/test_yaml_download_with_misc_info/NIV'
        bible = YAMLDownloader(default_directory=download_path, include_misc_info=True)
        bible.download_book('Philemon')
        document = yaml_file_interface.read('{0}/Philemon.yaml'.format(download_path))
        # For some reason, the misc. info is always placed after the passage contents in these tests?
        self.assertEqual('English', document['Info']['Language'], 'Language info is not correct')
        self.assertEqual('NIV', document['Info']['Translation'], 'Translation info is not correct')

    def test_yaml_download_with_different_file_path(self):
        download_path = './tmp/test_yaml_download_with_different_file_path/NIV'
        custom_path = './tmp/test_yaml_download_with_different_file_path.txt'
        bible = YAMLDownloader(default_directory=download_path)
        # File contents should remain the same with and without the custom path parameter
        bible.download_passage_range('1 John', 1, 3, 1, 5)
        bible.download_passage_range('1 John', 1, 3, 1, 5, file_path=custom_path)
        self.assertTrue(filecmp.cmp('{0}/1 John.yaml'.format(download_path), custom_path), 'Files do not match')
        # A default directory with a relative reference should also preserve the same file contents
        bible.default_directory = './tmp/../tmp/test_yaml_download_with_different_file_path/Fardel'
        bible.download_passage_range('1 John', 1, 3, 1, 5)
        self.assertTrue(filecmp.cmp('{0}/1 John.yaml'.format(bible.default_directory), custom_path),
                        'Files do not match')

    def test_yaml_download_with_excessive_values(self):
        download_path = './tmp/test_yaml_download_with_excessive_values/NIV'
        static_path = './static/NIV/test_yaml_download_with_excessive_values'
        branching_paths = [
            '{0}/Chapter-1'.format(download_path),
            '{0}/Chapter1000'.format(download_path),
            '{0}/Chapter5'.format(download_path),
        ]
        bible = YAMLDownloader(default_directory=branching_paths[0])
        # This should obtain the first passage of the first chapter
        bible.download_passage_range('1 John', -1, -1, -1, -1)
        self.assertTrue(filecmp.cmp('{0}/1 John.yaml'.format(bible.default_directory),
                                    '{0}/Chapter-1/1 John.yaml'.format(static_path)),
                        'Files do not match')
        # This does NOT get the last passage of the last chapter, but is instead deemed invalid.
        # This is consistent with how the Bible Gateway site handles when the starting passage is too high.
        bible.default_directory = branching_paths[1]
        self.assertRaises(InvalidSearchError, bible.download_passage_range, '1 John', 1000, 1000, 1000, 1000)
        # Gets the last chapter of the book.
        # This is valid because the starting passage is a correct number from the chapter.
        bible.default_directory = branching_paths[2]
        bible.download_passage_range('1 John', 1000, 1, 1000, 1000)
        self.assertTrue(filecmp.cmp('{0}/1 John.yaml'.format(bible.default_directory),
                                    '{0}/Chapter5/1 John.yaml'.format(static_path)),
                        'Files do not match')

if __name__ == "__main__":
    unittest.main()
