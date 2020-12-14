import unittest
import sys
import os
import filecmp
sys.path.append('../')
from meaningless import YAMLDownloader, yaml_file_interface, InvalidSearchError, InvalidPassageError


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    @staticmethod
    def get_test_translation():
        return 'WEB'

    @staticmethod
    def get_test_directory(translation='WEB'):
        return './static/unit_tests_bible_yaml_downloader/{0}'.format(translation)

    def test_yaml_download(self):
        download_path = './tmp/test_yaml_download/'
        bible = YAMLDownloader(default_directory=download_path, translation=self.get_test_translation())
        bible.download_book('Philemon')
        downloaded_yaml = yaml_file_interface.read('{0}/Philemon.yaml'.format(download_path))
        static_file_path = '{0}/test_yaml_download.yaml'.format(self.get_test_directory())
        static_yaml = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_yaml['Philemon'], static_yaml['Philemon'], 'Passage contents do not match')

    def test_yaml_download_without_passage_numbers(self):
        download_path = './tmp/test_yaml_download_without_passage_numbers/'
        bible = YAMLDownloader(default_directory=download_path, show_passage_numbers=False,
                               translation=self.get_test_translation())
        bible.download_book('Philemon')
        downloaded_yaml = yaml_file_interface.read('{0}/Philemon.yaml'.format(download_path))
        static_file_path = '{0}/test_yaml_download_without_passage_numbers.yaml'.format(self.get_test_directory())
        static_yaml = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_yaml['Philemon'], static_yaml['Philemon'], 'Passage contents do not match')

    def test_yaml_download_invalid_book(self):
        download_path = './tmp/test_yaml_download_invalid_book/'
        bible = YAMLDownloader(default_directory=download_path)
        # An invalid book should fail fast and not bother with downloading
        self.assertRaises(InvalidPassageError, bible.download_book, 'Barnabas')

    def test_yaml_download_kjv(self):
        download_path = './tmp/test_yaml_download_kjv/'
        bible = YAMLDownloader(default_directory=download_path, translation='kjv')
        bible.download_book('Philemon')
        downloaded_yaml = yaml_file_interface.read('{0}/Philemon.yaml'.format(download_path))
        static_file_path = '{0}/test_yaml_download_kjv.yaml'.format(self.get_test_directory('KJV'))
        static_yaml = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_yaml['Philemon'], static_yaml['Philemon'], 'Passage contents do not match')

    def test_yaml_download_omitted_passage(self):
        download_path = './tmp/test_yaml_download_omitted_passage/'
        bible = YAMLDownloader(default_directory=download_path, translation='NLT')
        bible.download_book('Romans')
        text = yaml_file_interface.read('{0}/Romans.yaml'.format(download_path))['Romans'][16][24]
        self.assertEqual('', text, 'Files do not match')

    def test_yaml_download_with_stripped_whitespaces(self):
        download_path = './tmp/test_yaml_download_with_stripped_whitespaces/'
        bible = YAMLDownloader(default_directory=download_path, strip_excess_whitespace=True,
                               translation=self.get_test_translation())
        bible.download_book('Philemon')
        downloaded_yaml = yaml_file_interface.read('{0}/Philemon.yaml'.format(download_path))
        static_file_path = '{0}/test_yaml_download_with_stripped_whitespaces.yaml'.format(self.get_test_directory())
        static_yaml = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_yaml['Philemon'], static_yaml['Philemon'], 'Passage contents do not match')

    def test_yaml_download_passage(self):
        download_path = './tmp/test_yaml_download_passage/'
        bible = YAMLDownloader(default_directory=download_path, translation=self.get_test_translation())
        bible.download_passage('Philemon', 1, 1)
        downloaded_yaml = yaml_file_interface.read('{0}/Philemon.yaml'.format(download_path))
        static_file_path = '{0}/test_yaml_download_passage.yaml'.format(self.get_test_directory())
        static_yaml = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_yaml['Philemon'], static_yaml['Philemon'], 'Passage contents do not match')

    def test_yaml_download_passages(self):
        download_path = './tmp/test_yaml_download_passages/'
        bible = YAMLDownloader(default_directory=download_path, translation=self.get_test_translation())
        bible.download_passages('Philemon', 1, 1, 3)
        downloaded_yaml = yaml_file_interface.read('{0}/Philemon.yaml'.format(download_path))
        static_file_path = '{0}/test_yaml_download_passages.yaml'.format(self.get_test_directory())
        static_yaml = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_yaml['Philemon'], static_yaml['Philemon'], 'Passage contents do not match')

    def test_yaml_download_chapter(self):
        download_path = './tmp/test_yaml_download_chapter/'
        bible = YAMLDownloader(default_directory=download_path, translation=self.get_test_translation())
        bible.download_chapter('1 John', 1)
        downloaded_yaml = yaml_file_interface.read('{0}/1 John.yaml'.format(download_path))
        static_file_path = '{0}/test_yaml_download_chapter.yaml'.format(self.get_test_directory())
        static_yaml = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_yaml['1 John'], static_yaml['1 John'], 'Passage contents do not match')

    def test_yaml_download_chapters(self):
        download_path = './tmp/test_yaml_download_chapters/'
        bible = YAMLDownloader(default_directory=download_path, translation=self.get_test_translation())
        bible.download_chapters('1 John', 1, 3)
        downloaded_yaml = yaml_file_interface.read('{0}/1 John.yaml'.format(download_path))
        static_file_path = '{0}/test_yaml_download_chapters.yaml'.format(self.get_test_directory())
        static_yaml = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_yaml['1 John'], static_yaml['1 John'], 'Passage contents do not match')

    def test_yaml_download_passage_range(self):
        download_path = './tmp/test_yaml_download_passage_range/'
        bible = YAMLDownloader(default_directory=download_path, translation=self.get_test_translation())
        bible.download_passage_range('1 John', 1, 3, 1, 5)
        downloaded_yaml = yaml_file_interface.read('{0}/1 John.yaml'.format(download_path))
        static_file_path = '{0}/test_yaml_download_passage_range.yaml'.format(self.get_test_directory())
        static_yaml = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_yaml['1 John'], static_yaml['1 John'], 'Passage contents do not match')

    def test_yaml_download_with_misc_info(self):
        download_path = './tmp/test_yaml_download_with_misc_info/NIV'
        bible = YAMLDownloader(default_directory=download_path)
        bible.download_passage('Philemon', 1, 1)
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
        download_path = './tmp/test_yaml_download_with_excessive_values/'
        static_path = '{0}/test_yaml_download_with_excessive_values'.format(self.get_test_directory())
        branching_paths = [
            '{0}/Chapter-1'.format(download_path),
            '{0}/Chapter1000'.format(download_path),
            '{0}/Chapter5'.format(download_path),
        ]
        bible = YAMLDownloader(default_directory=branching_paths[0], translation=self.get_test_translation())
        # This should obtain the first passage of the first chapter
        bible.download_passage_range('1 John', -1, -1, -1, -1)
        downloaded_yaml = yaml_file_interface.read('{0}/1 John.yaml'.format(bible.default_directory))
        static_yaml = yaml_file_interface.read('{0}/Chapter-1/1 John.yaml'.format(static_path))
        self.assertEqual(downloaded_yaml['1 John'], static_yaml['1 John'], 'Passage contents do not match')
        # This does NOT get the last passage of the last chapter, but is instead deemed invalid.
        # This is consistent with how the Bible Gateway site handles when the starting passage is too high.
        bible.default_directory = branching_paths[1]
        self.assertRaises(InvalidSearchError, bible.download_passage_range, '1 John', 1000, 1000, 1000, 1000)
        # Gets the last chapter of the book.
        # This is valid because the starting passage is a correct number from the chapter.
        bible.default_directory = branching_paths[2]
        bible.download_passage_range('1 John', 1000, 1, 1000, 1000)
        downloaded_yaml = yaml_file_interface.read('{0}/1 John.yaml'.format(bible.default_directory))
        static_yaml = yaml_file_interface.read('{0}/Chapter5/1 John.yaml'.format(static_path))
        self.assertEqual(downloaded_yaml['1 John'], static_yaml['1 John'], 'Passage contents do not match')

    def test_yaml_download_lowercase_translation(self):
        download_path = './tmp/test_yaml_download_lowercase_translation/NLT'
        bible = YAMLDownloader(default_directory=download_path, translation='NLT')
        bible.download_book('Philemon')
        bible.translation = 'nlt'
        lowercase_file_path = '{0}/Philemon-lowercase.yaml'.format(download_path)
        bible.download_book('Philemon', file_path=lowercase_file_path)
        self.assertTrue(filecmp.cmp('{0}/Philemon.yaml'.format(download_path), lowercase_file_path),
                        'Files do not match')

if __name__ == "__main__":
    unittest.main()
