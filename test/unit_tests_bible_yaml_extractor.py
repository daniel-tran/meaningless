import unittest
import sys
sys.path.append('../')
from meaningless import YAMLExtractor, UnsupportedTranslationError


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
        return './static/unit_tests_bible_yaml_extractor/{0}'.format(translation)

    def test_get_yaml_passage(self):
        bible = YAMLExtractor(default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_passage('Ecclesiastes', 2, 26)
        self.assertEqual('\u00b2\u2076 For to the man who pleases him, God gives wisdom, knowledge, and joy; but '
                         'to the sinner he gives travail, to gather and to heap up, that he may give to '
                         'him who pleases God. This also is vanity and a chasing after wind.', text,
                         'Passage is incorrect')

    def test_get_yaml_passages(self):
        bible = YAMLExtractor(default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_passages('Ecclesiastes', 2, 24, 25)
        self.assertEqual('\u00b2\u2074 There is nothing better for a man than that he should eat and drink, and '
                         'make his soul enjoy good in his labor. This also I saw, that it is from the '
                         'hand of God. '
                         '\u00b2\u2075 For who can eat, or who can have enjoyment, more than I?', text,
                         'Passage is incorrect')

    def test_get_yaml_chapter(self):
        bible = YAMLExtractor(default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_chapter('Ecclesiastes', 11)
        static_file = '{0}/test_get_yaml_chapter.txt'.format(self.get_test_directory())
        with open(static_file, 'r', encoding='utf-8') as file:
            eccl = file.read()
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_yaml_passage_range(self):
        bible = YAMLExtractor(default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_passage_range('Ecclesiastes', 9, 18, 10, 1)
        eccl = ['\u00b9\u2078 Wisdom is better than weapons of war; but one sinner destroys much good.',
                '\u00b9 Dead flies cause the oil of the perfumer to produce an evil odor;',
                '    so does a little folly outweigh wisdom and honor.'
                ]
        # This passage selection is on a chapter boundary, which means Ecclesiastes 9:18 has the trailing line character
        self.assertEqual('\n'.join(eccl), text, 'Passage is incorrect')

    def test_get_yaml_chapters(self):
        bible = YAMLExtractor(default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_chapters('Ecclesiastes', 11, 12)
        static_file = '{0}/test_get_yaml_chapters.txt'.format(self.get_test_directory())
        with open(static_file, 'r', encoding='utf-8') as file:
            eccl = file.read()
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_yaml_book(self):
        bible = YAMLExtractor(default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_book('Philemon')
        static_file = '{0}/test_get_yaml_book.txt'.format(self.get_test_directory())
        with open(static_file, 'r', encoding='utf-8') as file:
            phil = file.read()
        self.assertEqual(phil, text, 'Passage is incorrect')

    def test_get_yaml_passage_range_reverse_parameters(self):
        bible = YAMLExtractor(default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_passage_range('Ecclesiastes', 10, 1, 9, 18)
        # Chapter 10 is after chapter 9, so this should not work
        self.assertEqual('', text, 'Passage is incorrect')
        text = bible.get_passage_range('Ecclesiastes', 9, 2, 9, 1)
        # Verse 2 is after verse 1, so this should not work either
        self.assertEqual('', text, 'Passage is incorrect')

    def test_get_yaml_passage_range_negative_numbers(self):
        bible = YAMLExtractor(default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_passage_range('Ecclesiastes', 1, -1, 1, 1)
        eccl = '\u00b9 The words of the Preacher, the son of David, king in Jerusalem:'
        # This should apply value normalisation logic to ensure that negative values don't break the execution flow
        self.assertEqual(eccl, text, 'Passage is incorrect')
        text = bible.get_passage_range('Ecclesiastes', -1, 1, 1, 1)
        # Same normalisation should also apply for negative chapter numbers as well
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_yaml_passage_range_excessive_numbers(self):
        bible = YAMLExtractor(default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text = bible.get_passage_range('Ecclesiastes', 9000, 1, 9000, 2)
        sample1 = ['\u00b9 Remember also your Creator in the days of your youth,',
                   '    before the evil days come, and the years draw near,',
                   '    when you will say, \u201cI have no pleasure in them;\u201d',
                   '\u00b2 Before the sun, the light, the moon, and the stars are darkened,',
                   '    and the clouds return after the rain;']
        # Excessive chapters should just default to the last chapter of the book
        self.assertEqual('\n'.join(sample1), text, 'Passage is incorrect')
        text = bible.get_passage_range('Ecclesiastes', 1, 9000, 1, 9001)
        sample2 = '\u00b9\u2078 For in much wisdom is much grief; and he who increases knowledge increases sorrow.'
        # Excessive passages should just default to the last passage of the given chapter
        self.assertEqual(sample2, text, 'Passage is incorrect')

    def test_get_yaml_passage_invalid(self):
        bible = YAMLExtractor(default_directory=self.get_test_directory())
        self.assertRaises(FileNotFoundError, bible.get_passage, 'Barnabas', 2, 26)

    def test_get_yaml_passages_invalid(self):
        bible = YAMLExtractor(default_directory=self.get_test_directory())
        self.assertRaises(FileNotFoundError, bible.get_passages, 'Barnabas', 2, 26, 27)

    def test_get_yaml_chapter_invalid(self):
        bible = YAMLExtractor(default_directory=self.get_test_directory())
        self.assertRaises(FileNotFoundError, bible.get_chapter, 'Barnabas', 2)

    def test_get_yaml_chapters_invalid(self):
        bible = YAMLExtractor(default_directory=self.get_test_directory())
        self.assertRaises(FileNotFoundError, bible.get_chapters, 'Barnabas', 2, 3)

    def test_get_yaml_passage_range_invalid(self):
        bible = YAMLExtractor(default_directory=self.get_test_directory())
        self.assertRaises(FileNotFoundError, bible.get_passage_range, 'Barnabas', 2, 3, 2, 4)

    def test_get_yaml_passage_without_passage_numbers(self):
        bible = YAMLExtractor(show_passage_numbers=False, default_directory=self.get_test_directory(),
                              translation=self.get_test_translation())
        text = bible.get_passage('Ecclesiastes', 2, 26)
        self.assertEqual('For to the man who pleases him, God gives wisdom, knowledge, and joy; but '
                         'to the sinner he gives travail, to gather and to heap up, that he may give to '
                         'him who pleases God. This also is vanity and a chasing after wind.', text,
                         'Passage is incorrect')

    def test_get_yaml_passage_range_without_passage_numbers(self):
        bible = YAMLExtractor(show_passage_numbers=False, default_directory=self.get_test_directory(),
                              translation=self.get_test_translation())
        text = bible.get_passage_range('Ecclesiastes', 9, 18, 10, 1)
        eccl = ['Wisdom is better than weapons of war; but one sinner destroys much good.',
                'Dead flies cause the oil of the perfumer to produce an evil odor;',
                '    so does a little folly outweigh wisdom and honor.'
                ]
        self.assertEqual('\n'.join(eccl), text, 'Passage is incorrect')

    def test_get_yaml_passages_without_passage_numbers(self):
        bible = YAMLExtractor(show_passage_numbers=False, default_directory=self.get_test_directory(),
                              translation=self.get_test_translation())
        text = bible.get_passages('Ecclesiastes', 2, 24, 25)
        self.assertEqual('There is nothing better for a man than that he should eat and drink, and '
                         'make his soul enjoy good in his labor. This also I saw, that it is from the '
                         'hand of God. '
                         'For who can eat, or who can have enjoyment, more than I?', text, 'Passage is incorrect')

    def test_get_yaml_chapter_without_passage_numbers(self):
        bible = YAMLExtractor(show_passage_numbers=False, default_directory=self.get_test_directory(),
                              translation=self.get_test_translation())
        text = bible.get_chapter('Ecclesiastes', 11)
        static_file = '{0}/test_get_yaml_chapter_without_passage_numbers.txt'.format(self.get_test_directory())
        with open(static_file, 'r', encoding='utf-8') as file:
            eccl = file.read()
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_yaml_chapters_without_passage_numbers(self):
        bible = YAMLExtractor(show_passage_numbers=False, default_directory=self.get_test_directory(),
                              translation=self.get_test_translation())
        text = bible.get_chapters('Ecclesiastes', 11, 12)
        static_file = '{0}/test_get_yaml_chapters_without_passage_numbers.txt'.format(self.get_test_directory())
        with open(static_file, 'r', encoding='utf-8') as file:
            eccl = file.read()
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_yaml_passage_kjv(self):
        bible = YAMLExtractor(translation='KJV', default_directory=self.get_test_directory('KJV'))
        text = bible.get_passage('Ecclesiastes', 2, 26)
        self.assertEqual('\u00b2\u2076 For God giveth to a man that is good in his sight wisdom, and knowledge, '
                         'and joy: but to the sinner he giveth travail, to gather and to heap up, that '
                         'he may give to him that is good before God. This also is vanity and vexation '
                         'of spirit.', text,
                         'Passage is incorrect')

    def test_get_yaml_passage_invalid_translation(self):
        bible = YAMLExtractor(translation='LOL', default_directory=self.get_test_directory())
        self.assertRaises(UnsupportedTranslationError, bible.get_passage, 'Ecclesiastes', 2, 26)

    def test_get_yaml_passages_with_passage_separator(self):
        bible = YAMLExtractor(passage_separator='\n\n', default_directory=self.get_test_directory(),
                              translation=self.get_test_translation())
        text = bible.get_passages('Ecclesiastes', 2, 24, 25)
        eccl = ['\u00b2\u2074 There is nothing better for a man than that he should eat and drink, and '
                'make his soul enjoy good in his labor. This also I saw, that it is from the '
                'hand of God. ',
                '\u00b2\u2075 For who can eat, or who can have enjoyment, more than I?'
                ]
        # 1 new line character for the chapter boundary + 2 new lines for the passage separator
        self.assertEqual('\n\n'.join(eccl), text, 'Passage is incorrect')

    def test_get_yaml_passage_range_with_passage_separator_on_chapter_boundary(self):
        bible = YAMLExtractor(passage_separator='\n\n', default_directory=self.get_test_directory(),
                              translation=self.get_test_translation())
        text = bible.get_passage_range('Ecclesiastes', 9, 18, 10, 1)
        eccl = ['\u00b9\u2078 Wisdom is better than weapons of war; but one sinner destroys much good.',
                '\u00b9 Dead flies cause the oil of the perfumer to produce an evil odor;\n'
                '    so does a little folly outweigh wisdom and honor.'
                ]
        # Normally, the each chapter has a newline character auto appended on the end. With a passage separator,
        # this would be considered not necessary anymore, as the passage separator is used instead.
        self.assertEqual('\n\n'.join(eccl), text, 'Passage is incorrect')

    def test_get_yaml_passage_range_with_passage_separator_and_output_as_list(self):
        bible = YAMLExtractor(passage_separator='\n\n', output_as_list=True, default_directory=self.get_test_directory(),
                              translation=self.get_test_translation())
        text = bible.get_passage_range('Ecclesiastes', 9, 18, 10, 1)
        # Neither passage should have any trace of the passage separator, since the output is a list
        self.assertTrue((text[0].find('\n\n') < 0) and (text[1].find('\n\n') < 0),
                        'Passage separator should not have been found')

    def test_get_yaml_passage_lowercase_translation(self):
        bible = YAMLExtractor(translation='KJV', default_directory=self.get_test_directory('KJV'))
        text1 = bible.get_passage('Ecclesiastes', 2, 26)
        bible.translation = 'kjv'
        text2 = bible.get_passage('Ecclesiastes', 2, 26)
        # Translations should be case insensitive under the hood
        self.assertEqual(text1, text2, 'Passages do not match')

    def test_get_yaml_passage_range_with_file_path_param(self):
        bible = YAMLExtractor(default_directory=self.get_test_directory(), translation=self.get_test_translation())
        text1 = bible.get_passage('Ecclesiastes', 2, 26)
        # File path parameter should overwrite the default directory, regardless of what it was set to
        bible.default_directory = '../'
        yaml_file = '{0}/{1}'.format(self.get_test_directory(), 'Ecclesiastes.yaml')
        text2 = bible.get_passage('Ecclesiastes', 2, 26, yaml_file)
        # Translations should be case insensitive under the hood
        self.assertEqual(text1, text2, 'Passages do not match')

if __name__ == "__main__":
    unittest.main()
