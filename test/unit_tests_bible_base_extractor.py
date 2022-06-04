import unittest
import sys
sys.path.append('../')
from meaningless import UnsupportedTranslationError, TranslationMismatchError, InvalidPassageError
from meaningless.bible_base_extractor import BaseExtractor
from meaningless.utilities import yaml_file_interface, json_file_interface


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
        return './static/unit_tests_bible_base_extractor/{0}'.format(translation)

    @staticmethod
    def get_test_file_extension():
        """
        A helper function to consolidate the file extension used for the extractor
        :return: File extension with the leading dot
        :rtype: str
        """
        return '.yaml'

    def test_get_base_passage(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_passage('Ecclesiastes', 2, 26)
        self.assertEqual('²⁶ For to the man who pleases him, God gives wisdom, knowledge, and joy; but '
                         'to the sinner he gives travail, to gather and to heap up, that he may give to '
                         'him who pleases God. This also is vanity and a chasing after wind.', text,
                         'Passage is incorrect')

    def test_get_base_passages(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_passages('Ecclesiastes', 2, 24, 25)
        self.assertEqual('²⁴ There is nothing better for a man than that he should eat and drink, and '
                         'make his soul enjoy good in his labor. This also I saw, that it is from the '
                         'hand of God. '
                         '²⁵ For who can eat, or who can have enjoyment, more than I?', text,
                         'Passage is incorrect')

    def test_get_base_chapter(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_chapter('Ecclesiastes', 11)
        static_file = '{0}/test_get_base_chapter.txt'.format(self.get_test_directory())
        with open(static_file, 'r', encoding='utf-8') as file:
            eccl = file.read()
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_base_passage_range(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_passage_range('Ecclesiastes', 9, 18, 10, 1)
        eccl = ['¹⁸ Wisdom is better than weapons of war; but one sinner destroys much good.',
                '¹ Dead flies cause the oil of the perfumer to produce an evil odor;',
                '    so does a little folly outweigh wisdom and honor.'
                ]
        # This passage selection is on a chapter boundary, which means Ecclesiastes 9:18 has the trailing line character
        self.assertEqual('\n'.join(eccl), text, 'Passage is incorrect')

    def test_get_base_chapters(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_chapters('Ecclesiastes', 11, 12)
        static_file = '{0}/test_get_base_chapters.txt'.format(self.get_test_directory())
        with open(static_file, 'r', encoding='utf-8') as file:
            eccl = file.read()
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_base_book(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_book('Philemon')
        static_file = '{0}/test_get_base_book.txt'.format(self.get_test_directory())
        with open(static_file, 'r', encoding='utf-8') as file:
            phil = file.read()
        self.assertEqual(phil, text, 'Passage is incorrect')

    def test_get_base_passage_range_reverse_parameters(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_passage_range('Ecclesiastes', 10, 1, 9, 18)
        # Chapter 10 is after chapter 9, so this should not work
        self.assertEqual('', text, 'Passage is incorrect')
        text = bible.get_passage_range('Ecclesiastes', 9, 2, 9, 1)
        # Verse 2 is after verse 1, so this should not work either
        self.assertEqual('', text, 'Passage is incorrect')

    def test_get_base_passage_range_negative_numbers(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_passage_range('Ecclesiastes', 1, -1, 1, 1)
        eccl = '¹ The words of the Preacher, the son of David, king in Jerusalem:'
        # This should apply value normalisation logic to ensure that negative values don't break the execution flow
        self.assertEqual(eccl, text, 'Passage is incorrect')
        text = bible.get_passage_range('Ecclesiastes', -1, 1, 1, 1)
        # Same normalisation should also apply for negative chapter numbers as well
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_base_passage_range_excessive_numbers(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_passage_range('Ecclesiastes', 9000, 1, 9000, 2)
        sample1 = ['¹ Remember also your Creator in the days of your youth,',
                   '    before the evil days come, and the years draw near,',
                   '    when you will say, “I have no pleasure in them;”',
                   '² Before the sun, the light, the moon, and the stars are darkened,',
                   '    and the clouds return after the rain;']
        # Excessive chapters should just default to the last chapter of the book
        self.assertEqual('\n'.join(sample1), text, 'Passage is incorrect')
        text = bible.get_passage_range('Ecclesiastes', 1, 9000, 1, 9001)
        sample2 = '¹⁸ For in much wisdom is much grief; and he who increases knowledge increases sorrow.'
        # Excessive passages should just default to the last passage of the given chapter
        self.assertEqual(sample2, text, 'Passage is incorrect')

    def test_get_base_passage_invalid(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory())
        self.assertRaises(FileNotFoundError, bible.get_passage, 'Barnabas', 2, 26)

    def test_get_base_passages_invalid(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory())
        self.assertRaises(FileNotFoundError, bible.get_passages, 'Barnabas', 2, 26, 27)

    def test_get_base_chapter_invalid(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory())
        self.assertRaises(FileNotFoundError, bible.get_chapter, 'Barnabas', 2)

    def test_get_base_chapters_invalid(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory())
        self.assertRaises(FileNotFoundError, bible.get_chapters, 'Barnabas', 2, 3)

    def test_get_base_passage_range_invalid(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory())
        self.assertRaises(FileNotFoundError, bible.get_passage_range, 'Barnabas', 2, 3, 2, 4)

    def test_get_base_passage_without_passage_numbers(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              show_passage_numbers=False, default_directory=self.get_test_directory(),
                              translation=self.get_test_translation())
        text = bible.get_passage('Ecclesiastes', 2, 26)
        self.assertEqual('For to the man who pleases him, God gives wisdom, knowledge, and joy; but '
                         'to the sinner he gives travail, to gather and to heap up, that he may give to '
                         'him who pleases God. This also is vanity and a chasing after wind.', text,
                         'Passage is incorrect')

    def test_get_base_passage_range_without_passage_numbers(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              show_passage_numbers=False, default_directory=self.get_test_directory(),
                              translation=self.get_test_translation())
        text = bible.get_passage_range('Ecclesiastes', 9, 18, 10, 1)
        eccl = ['Wisdom is better than weapons of war; but one sinner destroys much good.',
                'Dead flies cause the oil of the perfumer to produce an evil odor;',
                '    so does a little folly outweigh wisdom and honor.'
                ]
        self.assertEqual('\n'.join(eccl), text, 'Passage is incorrect')

    def test_get_base_passages_without_passage_numbers(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              show_passage_numbers=False, default_directory=self.get_test_directory(),
                              translation=self.get_test_translation())
        text = bible.get_passages('Ecclesiastes', 2, 24, 25)
        self.assertEqual('There is nothing better for a man than that he should eat and drink, and '
                         'make his soul enjoy good in his labor. This also I saw, that it is from the '
                         'hand of God. '
                         'For who can eat, or who can have enjoyment, more than I?', text, 'Passage is incorrect')

    def test_get_base_chapter_without_passage_numbers(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              show_passage_numbers=False, default_directory=self.get_test_directory(),
                              translation=self.get_test_translation())
        text = bible.get_chapter('Ecclesiastes', 11)
        static_file = '{0}/test_get_base_chapter_without_passage_numbers.txt'.format(self.get_test_directory())
        with open(static_file, 'r', encoding='utf-8') as file:
            eccl = file.read()
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_base_chapters_without_passage_numbers(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              show_passage_numbers=False, default_directory=self.get_test_directory(),
                              translation=self.get_test_translation())
        text = bible.get_chapters('Ecclesiastes', 11, 12)
        static_file = '{0}/test_get_base_chapters_without_passage_numbers.txt'.format(self.get_test_directory())
        with open(static_file, 'r', encoding='utf-8') as file:
            eccl = file.read()
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_base_passage_kjv(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              translation='KJV', default_directory=self.get_test_directory('KJV'))
        text = bible.get_passage('Ecclesiastes', 2, 26)
        self.assertEqual('²⁶ For God giveth to a man that is good in his sight wisdom, and knowledge, '
                         'and joy: but to the sinner he giveth travail, to gather and to heap up, that '
                         'he may give to him that is good before God. This also is vanity and vexation '
                         'of spirit.', text,
                         'Passage is incorrect')

    def test_get_base_passage_invalid_translation(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              translation='LOL', default_directory=self.get_test_directory())
        self.assertRaises(UnsupportedTranslationError, bible.get_passage, 'Ecclesiastes', 2, 26)

    def test_get_base_passage_lowercase_translation(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              translation='KJV', default_directory=self.get_test_directory('KJV'))
        text1 = bible.get_passage('Ecclesiastes', 2, 26)
        bible.translation = 'kjv'
        text2 = bible.get_passage('Ecclesiastes', 2, 26)
        # Translations should be case insensitive under the hood
        self.assertEqual(text1, text2, 'Passages do not match')

    def test_get_base_passage_range_with_file_path_param(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text1 = bible.get_passage('Ecclesiastes', 2, 26)
        # File path parameter should overwrite the default directory, regardless of what it was set to
        bible.default_directory = '../'
        file = '{0}/{1}'.format(self.get_test_directory(), 'Ecclesiastes.yaml')
        text2 = bible.get_passage('Ecclesiastes', 2, 26, file)
        # Translations should be case insensitive under the hood
        self.assertEqual(text1, text2, 'Passages do not match')

    def test_get_base_passage_with_ascii_punctuation(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation(),
                              use_ascii_punctuation=True)
        text = bible.get_passage('Ecclesiastes', 1, 2)
        eccl = '² "Vanity of vanities," says the Preacher; "Vanity of vanities, all is vanity."'
        self.assertEqual(eccl, text, 'Passages do not match')

    def test_get_base_passage_with_string_keys(self):
        # Use the JSON file interface, which will only work if the keys are strings and not integers
        bible1 = BaseExtractor(file_reading_function=json_file_interface.read,
                               file_extension='.json',
                               default_directory=self.get_test_directory(), translation=self.get_test_translation(),
                               read_key_as_string=True)
        bible2 = BaseExtractor(file_reading_function=yaml_file_interface.read,
                               file_extension=self.get_test_file_extension(),
                               default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text1 = bible1.get_passage('Ecclesiastes', 1, 2)
        text2 = bible2.get_passage('Ecclesiastes', 1, 2)
        # Result should be the same when extracting the same passage from a file with string keys (with relevant
        # extractor settings) and from a file with integer keys
        self.assertEqual(text1, text2, 'Passages do not match')

    def test_get_base_passage_with_string_keys_mismatch(self):
        # Extractor should fail to work, since the JSON file interface can only read keys as strings
        bible1 = BaseExtractor(file_reading_function=json_file_interface.read,
                               file_extension='.json',
                               default_directory=self.get_test_directory(), translation=self.get_test_translation(),
                               read_key_as_string=False)
        # Extractor should fail to work, since the YAML file interface can only read keys as integers
        bible2 = BaseExtractor(file_reading_function=yaml_file_interface.read,
                               file_extension=self.get_test_file_extension(),
                               default_directory=self.get_test_directory(), translation=self.get_test_translation(),
                               read_key_as_string=True)
        self.assertRaises(KeyError, bible1.get_passage, 'Ecclesiastes', 1, 2)
        self.assertRaises(KeyError, bible2.get_passage, 'Ecclesiastes', 1, 2)

    def test_get_base_book_ascii_punctuation_count(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation(),
                              use_ascii_punctuation=False)
        text1 = bible.get_book('Ecclesiastes')
        bible.use_ascii_punctuation = True
        text2 = bible.get_book('Ecclesiastes')

        # Check that the punctuation conversion is a 1:1 translation
        self.assertEqual(text1.count('“') + text1.count('”'), text2.count('"'), 'Double quotes are unequal')
        self.assertEqual(text1.count('‘') + text1.count('’'), text2.count("'"), 'Single quotes are unequal')
        self.assertEqual(text1.count('—'), text2.count('-'), 'Dashes are unequal')

    def test_get_base_passage_buffered_first_passage(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              translation=self.get_test_translation())
        eccl = '² “Vanity of vanities,” says the Preacher; ' \
               '“Vanity of vanities, all is vanity.”'
        custom_file = '{0}/{1}'.format(self.get_test_directory(), 'test_get_base_passage_buffered_first_passage.yaml')
        text = bible.get_passage('Ecclesiastes', 1, 2, file_path=custom_file)
        # Custom file only contains one chapter and one passage, but doesn't start on the first passage
        self.assertEqual(text, eccl, 'Passages do not match')

    def test_get_base_passage_buffered_first_chapter(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              translation=self.get_test_translation())
        eccl = '² I said of laughter, “It is foolishness;” and of mirth, ' \
               '“What does it accomplish?”'
        custom_file = '{0}/{1}'.format(self.get_test_directory(), 'test_get_base_passage_buffered_first_chapter.yaml')
        text = bible.get_passage('Ecclesiastes', 2, 2, file_path=custom_file)
        # Custom file only contains one chapter and one passage, but doesn't start on the first passage or chapter
        self.assertEqual(text, eccl, 'Passages do not match')

    def test_get_base_passage_buffered_first_chapter_using_negative_parameters(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              translation=self.get_test_translation())
        eccl = '² I said of laughter, “It is foolishness;” and of mirth, ' \
               '“What does it accomplish?”'
        custom_file = '{0}/{1}'.format(self.get_test_directory(),
                                       'test_get_base_passage_buffered_first_chapter_using_negative_parameters.yaml')
        text = bible.get_passage_range('Ecclesiastes', -1, -1, -1, -1, file_path=custom_file)
        # All parameters should default to their minimum values, resulting in the first passage being returned
        self.assertEqual(text, eccl, 'Passages do not match')

    def test_get_base_passage_buffered_first_passage_using_chapter_interface(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              translation=self.get_test_translation())
        eccl = '² “Vanity of vanities,” says the Preacher; ' \
               '“Vanity of vanities, all is vanity.”'
        custom_file = '{0}/{1}'.format(self.get_test_directory(),
                                       'test_get_base_passage_buffered_first_passage_using_chapter_interface.yaml')
        text = bible.get_chapter('Ecclesiastes', 1, file_path=custom_file)
        # Custom file only contains one chapter and one passage, but should be able to detect that the passage count
        # doesn't start at 1
        self.assertEqual(text, eccl, 'Passages do not match')

    def test_get_base_passage_buffered_first_chapter_using_book_interface(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              translation=self.get_test_translation())
        eccl = '² I said of laughter, “It is foolishness;” and of mirth, ' \
               '“What does it accomplish?”'
        custom_file = '{0}/{1}'.format(self.get_test_directory(),
                                       'test_get_base_passage_buffered_first_chapter_using_book_interface.yaml')
        text = bible.get_book('Ecclesiastes', file_path=custom_file)
        # Custom file only contains one chapter and one passage, but should be able to detect that both the passage
        # and chapter count don't start at 1
        self.assertEqual(text, eccl, 'Passages do not match')

    def test_translation_mismatch_error(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        bible.translation = 'NLT'
        custom_file = '{0}/{1}'.format(self.get_test_directory(), 'Ecclesiastes.yaml')
        self.assertRaises(TranslationMismatchError, bible.get_passage, 'Ecclesiastes', 2, 2, custom_file)

    def test_translation_alias(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation='NRSVUE')
        # Read NRSV contents using an extractor using the NRSVUE translation
        custom_file = '{0}/{1}'.format(self.get_test_directory('NRSV'), 'Ecclesiastes.yaml')
        nrsv_text = bible.get_book('Ecclesiastes', file_path=custom_file)
        # Read NRSVUE contents using an extractor using the NRSV translation
        bible.translation = 'NRSV'
        custom_file = '{0}/{1}'.format(self.get_test_directory('NRSVUE'), 'Ecclesiastes.yaml')
        nrsvue_text = bible.get_book('Ecclesiastes', file_path=custom_file)
        self.assertEqual(nrsv_text, nrsvue_text, 'Passages do not match')

    def test_invalid_passage_error(self):
        bible = BaseExtractor(file_reading_function=json_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        # Test JSON file is specifically crafted to load nothing, yet is a valid document
        custom_file = '{0}/{1}'.format(self.get_test_directory(), 'test_invalid_passage_error.json')
        self.assertRaises(InvalidPassageError, bible.get_passage_range, 'Ecclesiastes', 1, 9000, 1, 9001, custom_file)
        self.assertRaises(InvalidPassageError, bible.get_passage_range, 'Ecclesiastes', 1, 1, 1, 1, custom_file)

    def test_find_text_in_passages(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        search_result = bible.find_text_in_passages('Vanity of vanities', 'Ecclesiastes', 1, 1, 3)
        expected_result = bible.get_passage('Ecclesiastes', 1, 2)
        self.assertEqual(expected_result, search_result, 'Passages do not match')

    def test_find_text_in_chapter(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        search_result = bible.find_text_in_chapter('Preacher', 'Ecclesiastes', 1)
        expected_result = '{0}\n{1}\n{2}'.format(bible.get_passage('Ecclesiastes', 1, 1),
                                                 bible.get_passage('Ecclesiastes', 1, 2),
                                                 bible.get_passage('Ecclesiastes', 1, 12))
        self.assertEqual(expected_result, search_result, 'Passages do not match')

    def test_find_text_in_chapters(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        search_result = bible.find_text_in_chapters('vanity', 'Ecclesiastes', 7, 8)
        expected_result = '{0}\n{1}\n{2}\n{3}'.format(bible.get_passage('Ecclesiastes', 7, 6),
                                                      bible.get_passage('Ecclesiastes', 7, 15),
                                                      bible.get_passage('Ecclesiastes', 8, 10),
                                                      bible.get_passage('Ecclesiastes', 8, 14))
        self.assertEqual(expected_result, search_result, 'Passages do not match')

    def test_find_text_in_book(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        search_result = bible.find_text_in_book('Preacher', 'Ecclesiastes')
        expected_result = '{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}'.format(bible.get_passage('Ecclesiastes', 1, 1),
                                                                     bible.get_passage('Ecclesiastes', 1, 2),
                                                                     bible.get_passage('Ecclesiastes', 1, 12),
                                                                     bible.get_passage('Ecclesiastes', 7, 27),
                                                                     bible.get_passage('Ecclesiastes', 12, 8),
                                                                     bible.get_passage('Ecclesiastes', 12, 9),
                                                                     bible.get_passage('Ecclesiastes', 12, 10))
        self.assertEqual(expected_result, search_result, 'Passages do not match')

    def test_find_text_in_passage_range(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        search_result = bible.find_text_in_passage_range('wisdom', 'Ecclesiastes', 1, 18, 2, 4)
        expected_result = '{0}\n{1}'.format(bible.get_passage('Ecclesiastes', 1, 18),
                                            bible.get_passage('Ecclesiastes', 2, 3))
        self.assertEqual(expected_result, search_result, 'Passages do not match')

    def test_find_text_in_passage_range_for_passage_number(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        search_result = bible.find_text_in_passage_range('²', 'Ecclesiastes', 1, 1, 1, 18)
        expected_result = '{0}\n{1}'.format(bible.get_passage('Ecclesiastes', 1, 2),
                                            bible.get_passage('Ecclesiastes', 1, 12))
        self.assertEqual(expected_result, search_result, 'Passages do not match')

        # Check that keyword searching takes into consideration the show_passage_numbers flag
        bible.show_passage_numbers = False
        search_result = bible.find_text_in_passage_range('²', 'Ecclesiastes', 1, 1, 1, 18)
        self.assertEqual('', search_result, 'Passages should not have been found')

    def test_find_text_in_passage_range_output_as_list(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation(),
                              output_as_list=True)
        search_result = bible.find_text_in_passage_range('wisdom', 'Ecclesiastes', 1, 18, 2, 4)
        expected_result = bible.get_passage('Ecclesiastes', 1, 18) + bible.get_passage('Ecclesiastes', 2, 3)
        self.assertEqual(expected_result, search_result, 'Passages do not match')

    def test_find_text_in_passage_range_no_match(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        search_result = bible.find_text_in_passage_range('Tyre', 'Ecclesiastes', 1, 1, 12, 14)
        expected_result = ''
        self.assertEqual(expected_result, search_result, 'Passages do not match')

    def test_find_text_in_passage_range_with_custom_file(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        file = '{0}/{1}'.format(self.get_test_directory(), 'test_find_text_in_passage_range_with_custom_file.yaml')
        search_result = bible.find_text_in_passage_range('One', 'Ecclesiastes', 1, 1, 1, 5, file)
        expected_result = bible.get_passage('Ecclesiastes', 1, 4, file)
        self.assertEqual(expected_result, search_result, 'Passages do not match')

    def test_find_text_in_passage_range_case_sensitive(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        search_result = bible.find_text_in_passage_range('all', 'Ecclesiastes', 1, 1, 1, 8, is_case_sensitive=True)
        expected_result = '{0}\n{1}\n{2}'.format(bible.get_passage('Ecclesiastes', 1, 2),
                                                 bible.get_passage('Ecclesiastes', 1, 3),
                                                 bible.get_passage('Ecclesiastes', 1, 6))
        # Expect to omit passages 7 and 8, since the search word is spelled as 'All'
        self.assertEqual(expected_result, search_result, 'Passages do not match')

    def test_find_text_in_passage_range_case_insensitive_regex(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        search_result = bible.find_text_in_passage_range(r'vanity|\sgain', 'Ecclesiastes', 1, 1, 1, 8, is_regex=True)
        expected_result = '{0}\n{1}'.format(bible.get_passage('Ecclesiastes', 1, 2),
                                            bible.get_passage('Ecclesiastes', 1, 3))
        self.assertEqual(expected_result, search_result, 'Passages do not match')

    def test_find_text_in_passage_range_case_sensitive_regex(self):
        bible = BaseExtractor(file_reading_function=yaml_file_interface.read,
                              file_extension=self.get_test_file_extension(),
                              default_directory=self.get_test_directory(), translation=self.get_test_translation())
        search_result = bible.find_text_in_passage_range('Vanity|There', 'Ecclesiastes', 1, 1, 1, 18,
                                                         is_regex=True, is_case_sensitive=True)
        expected_result = '{0}\n{1}'.format(bible.get_passage('Ecclesiastes', 1, 2),
                                            bible.get_passage('Ecclesiastes', 1, 11))
        self.assertEqual(expected_result, search_result, 'Passages do not match')


if __name__ == "__main__":
    unittest.main()
