import unittest
import sys
from timeit import default_timer
sys.path.append('../')
from meaningless import yaml_file_interface, InvalidSearchError, InvalidPassageError, UnsupportedTranslationError
from meaningless.bible_base_downloader import BaseDownloader


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    @staticmethod
    def get_test_translation():
        """
        A helper function to define the standardised translation for this set of tests.
        :return: Translation code
        :rtype: str
        """
        return 'WEB'

    @staticmethod
    def get_test_directory(translation='WEB'):
        """
        A helper function to determine the working directory for this set of unit tests
        :param translation: Translation code for the tests. For example, 'NIV', 'ESV', 'NLT'
        :type translation: str
        :return: Directory path containing readable files
        :rtype: str
        """
        return './static/unit_tests_bible_base_downloader/{0}'.format(translation)

    def test_base_download(self):
        download_path = './tmp/test_base_download/'
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path, translation=self.get_test_translation())
        bible.download_book('Philemon')
        downloaded_file = yaml_file_interface.read('{0}/Philemon'.format(download_path))
        static_file_path = '{0}/test_base_download.yaml'.format(self.get_test_directory())
        static_file = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_file['Philemon'], static_file['Philemon'], 'Passage contents do not match')

    def test_base_download_without_passage_numbers(self):
        download_path = './tmp/test_base_download_without_passage_numbers/'
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path, show_passage_numbers=False,
                               translation=self.get_test_translation())
        bible.download_book('Philemon')
        downloaded_file = yaml_file_interface.read('{0}/Philemon'.format(download_path))
        static_file_path = '{0}/test_base_download_without_passage_numbers.yaml'.format(self.get_test_directory())
        static_file = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_file['Philemon'], static_file['Philemon'], 'Passage contents do not match')

    def test_base_download_invalid_book(self):
        download_path = './tmp/test_base_download_invalid_book/'
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write, default_directory=download_path)
        # An invalid book should fail fast and not bother with downloading
        self.assertRaises(InvalidPassageError, bible.download_book, 'Barnabas')

    def test_base_download_kjv(self):
        download_path = './tmp/test_base_download_kjv/'
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path, translation='kjv')
        bible.download_book('Philemon')
        downloaded_file = yaml_file_interface.read('{0}/Philemon'.format(download_path))
        static_file_path = '{0}/test_base_download_kjv.yaml'.format(self.get_test_directory('KJV'))
        static_file = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_file['Philemon'], static_file['Philemon'], 'Passage contents do not match')

    def test_base_download_omitted_passage(self):
        download_path = './tmp/test_base_download_omitted_passage/'
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path, translation='NLT')
        bible.download_book('Romans')
        text = yaml_file_interface.read('{0}/Romans'.format(download_path))['Romans'][16][24]
        self.assertEqual('', text, 'Files do not match')

    def test_base_download_with_stripped_whitespaces(self):
        download_path = './tmp/test_base_download_with_stripped_whitespaces/'
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path, strip_excess_whitespace=True,
                               translation=self.get_test_translation())
        bible.download_book('Philemon')
        downloaded_file = yaml_file_interface.read('{0}/Philemon'.format(download_path))
        static_file_path = '{0}/test_base_download_with_stripped_whitespaces.yaml'.format(self.get_test_directory())
        static_file = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_file['Philemon'], static_file['Philemon'], 'Passage contents do not match')

    def test_base_download_passage(self):
        download_path = './tmp/test_base_download_passage/'
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path, translation=self.get_test_translation())
        bible.download_passage('Philemon', 1, 1)
        downloaded_file = yaml_file_interface.read('{0}/Philemon'.format(download_path))
        static_file_path = '{0}/test_base_download_passage.yaml'.format(self.get_test_directory())
        static_file = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_file['Philemon'], static_file['Philemon'], 'Passage contents do not match')

    def test_base_download_passages(self):
        download_path = './tmp/test_yaml_download_passages/'
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path, translation=self.get_test_translation())
        bible.download_passages('Philemon', 1, 1, 3)
        downloaded_file = yaml_file_interface.read('{0}/Philemon'.format(download_path))
        static_file_path = '{0}/test_base_download_passages.yaml'.format(self.get_test_directory())
        static_file = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_file['Philemon'], static_file['Philemon'], 'Passage contents do not match')

    def test_base_download_chapter(self):
        download_path = './tmp/test_base_download_chapter/'
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path, translation=self.get_test_translation())
        bible.download_chapter('1 John', 1)
        downloaded_file = yaml_file_interface.read('{0}/1 John'.format(download_path))
        static_file_path = '{0}/test_base_download_chapter.yaml'.format(self.get_test_directory())
        static_file = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_file['1 John'], static_file['1 John'], 'Passage contents do not match')

    def test_base_download_chapters(self):
        download_path = './tmp/test_base_download_chapters/'
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path, translation=self.get_test_translation())
        bible.download_chapters('1 John', 1, 3)
        downloaded_file = yaml_file_interface.read('{0}/1 John'.format(download_path))
        static_file_path = '{0}/test_base_download_chapters.yaml'.format(self.get_test_directory())
        static_file = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_file['1 John'], static_file['1 John'], 'Passage contents do not match')

    def test_base_download_passage_range(self):
        download_path = './tmp/test_base_download_passage_range/'
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path, translation=self.get_test_translation())
        bible.download_passage_range('1 John', 1, 3, 1, 5)
        downloaded_file = yaml_file_interface.read('{0}/1 John'.format(download_path))
        static_file_path = '{0}/test_base_download_passage_range.yaml'.format(self.get_test_directory())
        static_file = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_file['1 John'], static_file['1 John'], 'Passage contents do not match')

    def test_base_download_with_misc_info(self):
        download_path = './tmp/test_base_download_with_misc_info/NIV'
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path)
        bible.download_passage('Philemon', 1, 1)
        document = yaml_file_interface.read('{0}/Philemon'.format(download_path))
        # For some reason, the misc. info is always placed after the passage contents in these tests?
        self.assertEqual('English', document['Info']['Language'], 'Language info is not correct')
        self.assertEqual('NIV', document['Info']['Translation'], 'Translation info is not correct')

    def test_base_download_with_different_file_path(self):
        download_path = './tmp/test_base_download_with_different_file_path/NIV'
        custom_path = './tmp/test_base_download_with_different_file_path.txt'
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path)
        # File contents should remain the same with and without the custom path parameter
        book = '1 John'
        bible.download_passage_range(book, 1, 3, 1, 5)
        bible.download_passage_range(book, 1, 3, 1, 5, file_path=custom_path)
        self.assertEqual(yaml_file_interface.read('{0}/{1}'.format(download_path, book))[book],
                         yaml_file_interface.read(custom_path)[book],
                         'Files do not match')
        # A default directory with a relative reference should also preserve the same file contents
        bible.default_directory = './tmp/../tmp/test_base_download_with_different_file_path/Fardel'
        bible.download_passage_range(book, 1, 3, 1, 5)
        self.assertEqual(yaml_file_interface.read('{0}/{1}'.format(bible.default_directory, book))[book],
                         yaml_file_interface.read(custom_path)[book],
                         'Files do not match')

    def test_base_download_with_excessive_values(self):
        download_path = './tmp/test_base_download_with_excessive_values/'
        static_path = '{0}/test_base_download_with_excessive_values'.format(self.get_test_directory())
        branching_paths = [
            '{0}/Chapter-1'.format(download_path),
            '{0}/Chapter1000'.format(download_path),
            '{0}/Chapter5'.format(download_path),
        ]
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=branching_paths[0], translation=self.get_test_translation())
        # This should obtain the first passage of the first chapter
        bible.download_passage_range('1 John', -1, -1, -1, -1)
        downloaded_file = yaml_file_interface.read('{0}/1 John'.format(bible.default_directory))
        static_file = yaml_file_interface.read('{0}/Chapter-1/1 John.yaml'.format(static_path))
        self.assertEqual(downloaded_file['1 John'], static_file['1 John'], 'Passage contents do not match')
        # This does NOT get the last passage of the last chapter, but is instead deemed invalid.
        # This is consistent with how the Bible Gateway site handles when the starting passage is too high.
        bible.default_directory = branching_paths[1]
        self.assertRaises(InvalidSearchError, bible.download_passage_range, '1 John', 1000, 1000, 1000, 1000)
        # Gets the last chapter of the book.
        # This is valid because the starting passage is a correct number from the chapter.
        bible.default_directory = branching_paths[2]
        bible.download_passage_range('1 John', 1000, 1, 1000, 1000)
        downloaded_file = yaml_file_interface.read('{0}/1 John'.format(bible.default_directory))
        static_file = yaml_file_interface.read('{0}/Chapter5/1 John.yaml'.format(static_path))
        self.assertEqual(downloaded_file['1 John'], static_file['1 John'], 'Passage contents do not match')

    def test_base_download_lowercase_translation(self):
        download_path = './tmp/test_base_download_lowercase_translation/NLT'
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path, translation='NLT')
        book = 'Philemon'
        bible.download_book(book)
        bible.translation = 'nlt'
        lowercase_file_path = '{0}/{1}-lowercase'.format(download_path, book)
        bible.download_book(book, file_path=lowercase_file_path)
        self.assertEqual(yaml_file_interface.read('{0}/{1}'.format(download_path, book))[book],
                         yaml_file_interface.read(lowercase_file_path)[book],
                         'Files do not match')

    def test_base_download_single_process_benchmark(self):
        download_path = './tmp/test_base_download_single_process_benchmark'
        multi_processed_file = '{0}/multi_processed'.format(download_path)
        single_processed_file = '{0}/single_processed'.format(download_path)
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path, enable_multiprocessing=True)

        start = default_timer()
        book = 'Acts'
        bible.download_book(book, file_path=multi_processed_file)
        end = default_timer()
        multi_processed_time = end - start

        bible.enable_multiprocessing = False
        start = default_timer()
        bible.download_book(book, file_path=single_processed_file)
        end = default_timer()
        single_processed_time = end - start
        print('Multi-processed download took {0} seconds\n'
              'Single-processed download took {1} seconds'.format(multi_processed_time, single_processed_time))

        self.assertEqual(yaml_file_interface.read(multi_processed_file)[book],
                         yaml_file_interface.read(single_processed_file)[book],
                         'Files do not match')

    def test_base_download_with_ascii_punctuation(self):
        download_path = './tmp/test_base_download_with_ascii_punctuation'
        static_file_path = '{0}/test_base_download_with_ascii_punctuation.yaml'.format(self.get_test_directory())
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path, translation=self.get_test_translation(),
                               use_ascii_punctuation=True)
        bible.download_book('Ecclesiastes')
        downloaded_file = yaml_file_interface.read('{0}/Ecclesiastes'.format(download_path))
        static_file = yaml_file_interface.read(static_file_path)
        self.assertEqual(downloaded_file['Ecclesiastes'], static_file['Ecclesiastes'], 'Passage contents do not match')

    def test_base_download_with_string_keys(self):
        download_path = './tmp/test_base_download_with_string_keys'
        static_file_path = '{0}/test_base_download_with_string_keys.yaml'.format(self.get_test_directory())
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write,
                               default_directory=download_path, translation=self.get_test_translation(),
                               write_key_as_string=True)
        bible.download_chapter('Ecclesiastes', 1)
        downloaded_file = yaml_file_interface.read('{0}/Ecclesiastes'.format(download_path))
        static_file = yaml_file_interface.read(static_file_path)
        # Downloaded YAML files normally preserve integer keys, so check that passage access with string keys is OK
        self.assertEqual(downloaded_file['Ecclesiastes']['1']['2'], static_file['Ecclesiastes']['1']['2'],
                         'Passage sample does not match')
        self.assertEqual(downloaded_file['Ecclesiastes'], static_file['Ecclesiastes'], 'Passage contents do not match')

    def test_unsupported_translation(self):
        download_path = './tmp/test_unsupported_translation/'
        bible = BaseDownloader(file_writing_function=yaml_file_interface.write, default_directory=download_path,
                               translation='test_unsupported_translation')
        self.assertRaises(UnsupportedTranslationError, bible.download_book, 'Ecclesiastes')


if __name__ == "__main__":
    unittest.main()
