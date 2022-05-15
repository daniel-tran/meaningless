import unittest
import multiprocessing
import sys
sys.path.append('../')
from meaningless import WebExtractor, YAMLDownloader, YAMLExtractor
from meaningless.utilities import common


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def check_with_static_passage_contents(self, translation, book, chapter=1, passage=1, actual_result='',
                                           is_baseline=False):
        """
        Checks that a given passage result matches the expected data in a corresponding static file

        :param translation: Translation code for the tests. For example, 'NIV', 'ESV', 'NLT'
        :type translation: str
        :param book: Name of the book. Dual-purposed as the baseline test index when is_baseline is True.
        :type book: str
        :param chapter: Chapter number. Defaults to 1.
        :type chapter: int
        :param passage: Passage number. Defaults to 1.
        :type passage: int
        :param actual_result: Passage result from an extractor. Defaults to the empty string
        :type actual_result: str
        :param is_baseline: Indicates whether a baseline passage is in use. Defaults to False.
        :type is_baseline: bool
        """
        if is_baseline:
            # Baseline passages use a more generic file name, since the intention is to test a specific passage type.
            # The book is re-purposed as the baseline test index so that the parameters are still fairly intuitive
            # when invoking this method.
            static_file = './static/system_tests_bible_translations/{0}/passage_baseline_{1}.txt'.format(translation,
                                                                                                       book)
        else:
            static_file = './static/system_tests_bible_translations/{0}/passage_{1}_{2}_{3}.txt'.format(translation, book,
                                                                                                      chapter, passage)
        with open(static_file, 'r', encoding='utf-8') as file:
            contents = file.read()
        self.assertEqual(contents, actual_result, 'Passage is incorrect')

    def check_baseline_passages(self, translation):
        """
        Checks that a translation can return the correct results for a basic set of passages

        :param translation: Translation code for the tests. For example, 'NIV', 'ESV', 'NLT'
        :type translation: str
        """
        bible = WebExtractor(translation=translation)
        # Searching is language independent, so any translation can search using the English book names
        actual_passage_results = [
            bible.search('Revelation 21:25'),
            bible.search('Matthew 1:1 - 3'),
            bible.search('Nehemiah 7:40 - 42'),
            bible.search('Psalm 32:4'),
            bible.search('John 7:53')
        ]
        for expected_passage_index in range(0, len(actual_passage_results)):
            self.check_with_static_passage_contents(translation, str(expected_passage_index),
                                                    actual_result=actual_passage_results[expected_passage_index],
                                                    is_baseline=True)

    def check_omitted_passages(self, translation):
        """
        Checks that a translation can return the correct results for all known passages which can be omitted

        :param translation: Translation code for the tests. For example, 'NIV', 'ESV', 'NLT'
        :type translation: str
        """
        download_path = './tmp/check_omitted_passages/{0}'.format(translation)
        # Downloading the books with a process map is somewhat faster than using multiple daemon processes to
        # acquire each book sequentially.
        downloader = YAMLDownloader(translation=translation, enable_multiprocessing=False,
                                    default_directory=download_path)
        bible = YAMLExtractor(translation=translation, default_directory=download_path)

        if common.is_supported_spanish_translation(translation):
            books_with_omissions = ['Mateo', 'Marcos', 'Lucas', 'Juan', 'Hechos', 'Romanos']
        else:
            books_with_omissions = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans']
        pool = multiprocessing.Pool(len(books_with_omissions))
        pool.map(downloader.download_book, books_with_omissions)
        # Wait for the processes to complete and clean up the pool to prevent potential resource leaking
        pool.close()
        pool.join()

        # Matthew
        book = books_with_omissions[0]
        self.check_with_static_passage_contents(translation, book, 9, 34, bible.get_passage(book, 9, 34), False)
        self.check_with_static_passage_contents(translation, book, 12, 47, bible.get_passage(book, 12, 47), False)
        self.check_with_static_passage_contents(translation, book, 17, 21, bible.get_passage(book, 17, 21), False)
        self.check_with_static_passage_contents(translation, book, 18, 11, bible.get_passage(book, 18, 11), False)
        self.check_with_static_passage_contents(translation, book, 21, 44, bible.get_passage(book, 21, 44), False)
        self.check_with_static_passage_contents(translation, book, 23, 14, bible.get_passage(book, 23, 14), False)

        # Mark
        book = books_with_omissions[1]
        self.check_with_static_passage_contents(translation, book, 7, 16, bible.get_passage(book, 7, 16), False)
        self.check_with_static_passage_contents(translation, book, 9, 44, bible.get_passage(book, 9, 44), False)
        self.check_with_static_passage_contents(translation, book, 9, 46, bible.get_passage(book, 9, 46), False)
        self.check_with_static_passage_contents(translation, book, 11, 26, bible.get_passage(book, 11, 26), False)
        self.check_with_static_passage_contents(translation, book, 15, 28, bible.get_passage(book, 15, 28), False)
        self.check_with_static_passage_contents(translation, book, 16, 9, bible.get_passage(book, 16, 9), False)
        self.check_with_static_passage_contents(translation, book, 16, 20, bible.get_passage(book, 16, 20), False)

        # Luke
        book = books_with_omissions[2]
        self.check_with_static_passage_contents(translation, book, 17, 36, bible.get_passage(book, 17, 36), False)
        self.check_with_static_passage_contents(translation, book, 22, 20, bible.get_passage(book, 22, 20), False)
        self.check_with_static_passage_contents(translation, book, 22, 43, bible.get_passage(book, 22, 43), False)
        self.check_with_static_passage_contents(translation, book, 22, 44, bible.get_passage(book, 22, 44), False)
        self.check_with_static_passage_contents(translation, book, 23, 17, bible.get_passage(book, 23, 17), False)
        self.check_with_static_passage_contents(translation, book, 24, 12, bible.get_passage(book, 24, 12), False)
        self.check_with_static_passage_contents(translation, book, 24, 40, bible.get_passage(book, 24, 40), False)

        # John
        book = books_with_omissions[3]
        self.check_with_static_passage_contents(translation, book, 5, 4, bible.get_passage(book, 5, 4), False)
        self.check_with_static_passage_contents(translation, book, 7, 53, bible.get_passage(book, 7, 53), False)
        self.check_with_static_passage_contents(translation, book, 8, 11, bible.get_passage(book, 8, 11), False)

        # Acts
        book = books_with_omissions[4]
        self.check_with_static_passage_contents(translation, book, 8, 37, bible.get_passage(book, 8, 37), False)
        self.check_with_static_passage_contents(translation, book, 15, 34, bible.get_passage(book, 15, 34), False)
        self.check_with_static_passage_contents(translation, book, 24, 7, bible.get_passage(book, 24, 7), False)
        self.check_with_static_passage_contents(translation, book, 28, 29, bible.get_passage(book, 28, 29), False)

        # Romans
        book = books_with_omissions[5]
        self.check_with_static_passage_contents(translation, book, 16, 24, bible.get_passage(book, 16, 24), False)

    def test_translation_niv(self):
        translation = 'NIV'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_nasb(self):
        translation = 'NASB'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_nkjv(self):
        translation = 'NKJV'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_nrsv(self):
        translation = 'NRSV'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_esv(self):
        translation = 'ESV'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_web(self):
        translation = 'WEB'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_nlt(self):
        translation = 'NLT'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_kjv(self):
        translation = 'KJV'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_asv(self):
        translation = 'ASV'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_ylt(self):
        translation = 'YLT'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_net(self):
        translation = 'NET'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_nlv(self):
        translation = 'NLV'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_kj21(self):
        translation = 'KJ21'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_akjv(self):
        translation = 'AKJV'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_mev(self):
        translation = 'MEV'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_leb(self):
        translation = 'LEB'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_brg(self):
        translation = 'BRG'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_ehv(self):
        translation = 'EHV'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_esvuk(self):
        translation = 'ESVUK'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_gw(self):
        translation = 'GW'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_isv(self):
        translation = 'ISV'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_jub(self):
        translation = 'JUB'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_nog(self):
        translation = 'NOG'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_nasb1995(self):
        translation = 'NASB1995'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_cjb(self):
        translation = 'CJB'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_gnv(self):
        translation = 'GNV'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_rva(self):
        translation = 'RVA'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_nivuk(self):
        translation = 'NIVUK'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)

    def test_translation_nrsvue(self):
        translation = 'NRSVUE'
        self.check_baseline_passages(translation)
        self.check_omitted_passages(translation)


if __name__ == "__main__":
    unittest.main()
