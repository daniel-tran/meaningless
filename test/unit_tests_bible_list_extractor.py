import unittest
import sys
import os
import filecmp
sys.path.append('../')
from meaningless import YAMLExtractor, WebExtractor, InvalidSearchError


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    @staticmethod
    def test_directory(translation='NIV'):
        return './static/unit_tests_bible_list_extractor/{0}'.format(translation)

    def test_get_passage_list_from_string(self):
        bible = WebExtractor(output_as_list=True)
        text = bible.search('1 John 1:8 - 9')
        john = ['\u2078 If we claim to be without sin, we deceive ourselves and the truth is not in us. ',
                '\u2079 If we confess our sins, he is faithful and just and will forgive us our sins and purify '
                'us from all unrighteousness.']
        self.assertEqual(john, text, 'Passage is incorrect')

    def test_get_passage_list_from_string_empty(self):
        bible = WebExtractor(output_as_list=True)
        self.assertRaises(InvalidSearchError, bible.search, '')

    def test_get_passage_list_from_string_without_passage_numbers(self):
        bible = WebExtractor(output_as_list=True, show_passage_numbers=False)
        text = bible.search('Haggai 1:3 - 4')
        haggai1 = ['Then the word of the Lord came through the prophet Haggai: ',
                   '\u201cIs it a time for you yourselves to be living in your paneled houses, '
                   'while this house remains a ruin?\u201d']
        self.assertEqual(haggai1, text, 'Passage is incorrect')

    def test_get_passage_list_from_string_nlt(self):
        bible = WebExtractor(output_as_list=True, translation='NLT')
        text = bible.search('1 John 1:8 - 9')
        john = ['\u2078 If we claim we have no sin, we are only fooling ourselves and not living in the truth. ',
                '\u2079 But if we confess our sins to him, he is faithful and just to forgive us our sins and '
                'to cleanse us from all wickedness.']
        self.assertEqual(john, text, 'Passage is incorrect')

    def test_get_passage_list(self):
        bible = WebExtractor(output_as_list=True)
        text = bible.get_passage('1 John', 1, 8)
        john = ['\u2078 If we claim to be without sin, we deceive ourselves and the truth is not in us.']
        self.assertEqual(john, text, 'Passage is incorrect')

    def test_get_passages_list(self):
        bible = WebExtractor(output_as_list=True)
        text = bible.get_passages('1 John', 1, 8, 9)
        john = ['\u2078 If we claim to be without sin, we deceive ourselves and the truth is not in us. ',
                '\u2079 If we confess our sins, he is faithful and just and will forgive us our sins and purify '
                'us from all unrighteousness.']
        self.assertEqual(john, text, 'Passage is incorrect')

    def test_get_chapter_list(self):
        bible = WebExtractor(output_as_list=True)
        text = bible.get_chapter('Ecclesiastes', 11)
        eccl11 = ['Ship your grain across the sea;\n'
                  '    after many days you may receive a return.\n',
                  '\u00b2 Invest in seven ventures, yes, in eight;\n'
                  '    you do not know what disaster may come upon the land. \n',
                  '\u00b3 If clouds are full of water,\n'
                  '    they pour rain on the earth.\n'
                  'Whether a tree falls to the south or to the north,\n'
                  '    in the place where it falls, there it will lie.\n',
                  '\u2074 Whoever watches the wind will not plant;\n'
                  '    whoever looks at the clouds will not reap. \n',
                  '\u2075 As you do not know the path of the wind,\n'
                  '    or how the body is formed in a mother\u2019s womb,\n'
                  'so you cannot understand the work of God,\n'
                  '    the Maker of all things. \n',
                  '\u2076 Sow your seed in the morning,\n'
                  '    and at evening let your hands not be idle,\n'
                  'for you do not know which will succeed,\n'
                  '    whether this or that,\n'
                  '    or whether both will do equally well. \n',
                  '\u2077 Light is sweet,\n'
                  '    and it pleases the eyes to see the sun.\n',
                  '\u2078 However many years anyone may live,\n'
                  '    let them enjoy them all.\nBut let them remember the days of darkness,\n'
                  '    for there will be many.\n'
                  '    Everything to come is meaningless. \n',
                  '\u2079 You who are young, be happy while you are young,\n'
                  '    and let your heart give you joy in the days of your youth.\n'
                  'Follow the ways of your heart\n'
                  '    and whatever your eyes see,\n'
                  'but know that for all these things\n'
                  '    God will bring you into judgment.\n',
                  '\u00b9\u2070 So then, banish anxiety from your heart\n'
                  '    and cast off the troubles of your body,\n'
                  '    for youth and vigor are meaningless.'
                  ]
        self.assertEqual(eccl11, text, 'Passage is incorrect')

    def test_get_chapters_list(self):
        bible = WebExtractor(output_as_list=True)
        text = bible.get_chapters('1 John', 1, 2)
        john = bible.get_chapter('1 John', 1) + bible.get_chapter('1 John', 2)
        # Getting multiple sequential chapters should be the same as appending multiple chapters manually
        self.assertEqual(john, text, 'Passage is incorrect')

    def test_get_passage_range_list(self):
        bible = WebExtractor(output_as_list=True)
        text = bible.get_passage_range('Ecclesiastes', 9, 18, 10, 1)
        eccl = ['\u00b9\u2078 Wisdom is better than weapons of war,\n'
                '    but one sinner destroys much good.',
                'As dead flies give perfume a bad smell,\n'
                '    so a little folly outweighs wisdom and honor.'
                ]
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_book_list(self):
        bible = WebExtractor(output_as_list=True)
        text = bible.get_book('Philemon')
        with open('./static/NIV/test_get_book_list.txt', 'r', encoding='utf-8') as file:
            phil = file.read()
        # To avoid having to paste the entire contents of Philemon in the test, this is tested by joining all the
        # lines of the list into a single string and comparing against a test file
        self.assertEqual(phil, ''.join(text), 'Passage is incorrect')

    def test_get_passage_range_list_from_same_chapter(self):
        bible = WebExtractor(output_as_list=True)
        text = bible.get_passage_range('1 John', 1, 8, 1, 9)
        john = ['\u2078 If we claim to be without sin, we deceive ourselves and the truth is not in us. ',
                '\u2079 If we confess our sins, he is faithful and just and will forgive us our sins and purify '
                'us from all unrighteousness.']
        self.assertEqual(john, text, 'Passage is incorrect')

    def test_get_passages_list_with_stripped_whitespace(self):
        bible = WebExtractor(output_as_list=True, strip_excess_whitespace_from_list=True)
        text = bible.get_passages('Ecclesiastes', 11, 6, 7)
        eccl11 = ['\u2076 Sow your seed in the morning,\n'
                  '    and at evening let your hands not be idle,\n'
                  'for you do not know which will succeed,\n'
                  '    whether this or that,\n'
                  '    or whether both will do equally well.',
                  '\u2077 Light is sweet,\n'
                  '    and it pleases the eyes to see the sun.'
                  ]
        # These two passages are normally in a poetic format, each ending with a newline.
        # Toggling the flag parameter should not preserve these newline characters, but the inner newlines are kept.
        self.assertEqual(eccl11, text, 'Passage is incorrect')

    def test_get_yaml_passage_list(self):
        bible = YAMLExtractor(output_as_list=True, default_directory=self.test_directory())
        text = bible.get_passage('1 John', 1, 8)
        john = ['\u2078 If we claim to be without sin, we deceive ourselves and the truth is not in us. ']
        self.assertEqual(john, text, 'Passage is incorrect')

    def test_get_yaml_passages_list(self):
        bible = YAMLExtractor(output_as_list=True, default_directory=self.test_directory())
        text = bible.get_passages('1 John', 1, 8, 9)
        john = ['\u2078 If we claim to be without sin, we deceive ourselves and the truth is not in us. ',
                '\u2079 If we confess our sins, he is faithful and just and will forgive us our sins and purify '
                'us from all unrighteousness. ']
        self.assertEqual(john, text, 'Passage is incorrect')

    def test_get_yaml_chapter_list(self):
        online_bible = WebExtractor(output_as_list=True, show_passage_numbers=False)
        yaml_bible = YAMLExtractor(output_as_list=True, show_passage_numbers=False,
                                   default_directory=self.test_directory())
        text = yaml_bible.get_chapter('Ecclesiastes', 11)
        eccl = online_bible.get_chapter('Ecclesiastes', 11)
        # Results should be identical between the web and YAML extractor
        # Ignoring passage numbers, as the web extractor omits this for the first passage of each chapter
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_yaml_chapters_list(self):
        online_bible = WebExtractor(output_as_list=True, show_passage_numbers=False)
        yaml_bible = YAMLExtractor(output_as_list=True, show_passage_numbers=False,
                                   default_directory=self.test_directory())
        text = yaml_bible.get_chapters('Ecclesiastes', 11, 12)
        eccl = online_bible.get_chapters('Ecclesiastes', 11, 12)
        # Results should be identical between the web and YAML extractor
        # Ignoring passage numbers, as the web extractor omits this for the first passage of each chapter
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_yaml_book_list(self):
        online_bible = WebExtractor(output_as_list=True)
        yaml_bible = YAMLExtractor(output_as_list=True, default_directory=self.test_directory())
        text = yaml_bible.get_book('Philemon')
        eccl = online_bible.get_book('Philemon')
        # Results should be identical between the web and YAML extractor
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_yaml_passage_range_list(self):
        yaml_bible = YAMLExtractor(output_as_list=True, default_directory=self.test_directory())
        text = yaml_bible.get_passage_range('Ecclesiastes', 9, 18, 10, 1)
        eccl = ['\u00b9\u2078 Wisdom is better than weapons of war,\n'
                '    but one sinner destroys much good.',
                '\u00b9 As dead flies give perfume a bad smell,\n'
                '    so a little folly outweighs wisdom and honor.\n'
                ]
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_yaml_passage_range_list_with_stripped_whitespace(self):
        yaml_bible = YAMLExtractor(output_as_list=True, strip_excess_whitespace_from_list=True,
                                   default_directory=self.test_directory())
        text = yaml_bible.get_passage_range('Ecclesiastes', 10, 1, 10, 2)
        eccl = ['\u00b9 As dead flies give perfume a bad smell,\n'
                '    so a little folly outweighs wisdom and honor.',
                '\u00b2 The heart of the wise inclines to the right,\n'
                '    but the heart of the fool to the left.'
                ]
        self.assertEqual(eccl, text, 'Passage is incorrect')

if __name__ == "__main__":
    unittest.main()
