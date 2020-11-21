import unittest
import sys
import os
sys.path.append('../src/')
from meaningless import bible_yaml_extractor


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def test_get_yaml_passage(self):
        text = bible_yaml_extractor.get_yaml_passage('Ecclesiastes', 2, 26)
        self.assertEqual('\u00b2\u2076 To the person who pleases him, God gives wisdom, knowledge and happiness, '
                         'but to the sinner he gives the task of gathering and storing up wealth to hand '
                         'it over to the one who pleases God. This too is meaningless, a chasing after '
                         'the wind.', text, 'Passage is incorrect')

    def test_get_yaml_passages(self):
        text = bible_yaml_extractor.get_yaml_passages('Ecclesiastes', 2, 24, 25)
        self.assertEqual('\u00b2\u2074 A person can do nothing better than to eat and drink and find satisfaction '
                         'in their own toil. This too, I see, is from the hand of God, '
                         '\u00b2\u2075 for without him, who can eat or find enjoyment?', text, 'Passage is incorrect')

    def test_get_yaml_chapter(self):
        text = bible_yaml_extractor.get_yaml_chapter('Ecclesiastes', 11)
        eccl11 = ['Ship your grain across the sea;',
                  '    after many days you may receive a return.',
                  '\u00b2 Invest in seven ventures, yes, in eight;',
                  '    you do not know what disaster may come upon the land. ',
                  '\u00b3 If clouds are full of water,',
                  '    they pour rain on the earth.',
                  'Whether a tree falls to the south or to the north,',
                  '    in the place where it falls, there it will lie.',
                  '\u2074 Whoever watches the wind will not plant;',
                  '    whoever looks at the clouds will not reap. ',
                  '\u2075 As you do not know the path of the wind,',
                  '    or how the body is formed in a mother\u2019s womb,',
                  'so you cannot understand the work of God,',
                  '    the Maker of all things. ',
                  '\u2076 Sow your seed in the morning,',
                  '    and at evening let your hands not be idle,',
                  'for you do not know which will succeed,',
                  '    whether this or that,',
                  '    or whether both will do equally well. ',
                  '\u2077 Light is sweet,',
                  '    and it pleases the eyes to see the sun.',
                  '\u2078 However many years anyone may live,',
                  '    let them enjoy them all.\nBut let them remember the days of darkness,',
                  '    for there will be many.',
                  '    Everything to come is meaningless. ',
                  '\u2079 You who are young, be happy while you are young,',
                  '    and let your heart give you joy in the days of your youth.',
                  'Follow the ways of your heart',
                  '    and whatever your eyes see,',
                  'but know that for all these things',
                  '    God will bring you into judgment.',
                  '\u00b9\u2070 So then, banish anxiety from your heart',
                  '    and cast off the troubles of your body,',
                  '    for youth and vigor are meaningless.'
                  ]
        self.assertEqual('\n'.join(eccl11), text, 'Passage is incorrect')

    def test_get_yaml_passage_range(self):
        text = bible_yaml_extractor.get_yaml_passage_range('Ecclesiastes', 9, 18, 10, 1)
        eccl = ['\u00b9\u2078 Wisdom is better than weapons of war,',
                '    but one sinner destroys much good.',
                'As dead flies give perfume a bad smell,',
                '    so a little folly outweighs wisdom and honor.'
                ]
        # This passage selection is on a chapter boundary, which means Ecclesiastes 9:18 has the trailing line character
        self.assertEqual('\n'.join(eccl), text, 'Passage is incorrect')

    def test_get_yaml_chapters(self):
        text = bible_yaml_extractor.get_yaml_chapters('Ecclesiastes', 11, 12)
        eccl11_12 = ['Ship your grain across the sea;',
                     '    after many days you may receive a return.',
                     '\u00b2 Invest in seven ventures, yes, in eight;',
                     '    you do not know what disaster may come upon the land. ',
                     '\u00b3 If clouds are full of water,',
                     '    they pour rain on the earth.',
                     'Whether a tree falls to the south or to the north,',
                     '    in the place where it falls, there it will lie.',
                     '\u2074 Whoever watches the wind will not plant;',
                     '    whoever looks at the clouds will not reap. ',
                     '\u2075 As you do not know the path of the wind,',
                     '    or how the body is formed in a mother\u2019s womb,',
                     'so you cannot understand the work of God,',
                     '    the Maker of all things. ',
                     '\u2076 Sow your seed in the morning,',
                     '    and at evening let your hands not be idle,',
                     'for you do not know which will succeed,',
                     '    whether this or that,',
                     '    or whether both will do equally well. ',
                     '\u2077 Light is sweet,',
                     '    and it pleases the eyes to see the sun.',
                     '\u2078 However many years anyone may live,',
                     '    let them enjoy them all.\nBut let them remember the days of darkness,',
                     '    for there will be many.',
                     '    Everything to come is meaningless. ',
                     '\u2079 You who are young, be happy while you are young,',
                     '    and let your heart give you joy in the days of your youth.',
                     'Follow the ways of your heart',
                     '    and whatever your eyes see,',
                     'but know that for all these things',
                     '    God will bring you into judgment.',
                     '\u00b9\u2070 So then, banish anxiety from your heart',
                     '    and cast off the troubles of your body,',
                     '    for youth and vigor are meaningless.',
                     # Chapter 12
                     'Remember your Creator',
                     '    in the days of your youth,',
                     'before the days of trouble come',
                     '    and the years approach when you will say,',
                     '    \u201cI find no pleasure in them\u201d\u2014',
                     '\u00b2 before the sun and the light',
                     '    and the moon and the stars grow dark,',
                     '    and the clouds return after the rain;',
                     '\u00b3 when the keepers of the house tremble,',
                     '    and the strong men stoop,',
                     'when the grinders cease because they are few,',
                     '    and those looking through the windows grow dim;',
                     '\u2074 when the doors to the street are closed',
                     '    and the sound of grinding fades;',
                     'when people rise up at the sound of birds,',
                     '    but all their songs grow faint;',
                     '\u2075 when people are afraid of heights',
                     '    and of dangers in the streets;',
                     'when the almond tree blossoms',
                     '    and the grasshopper drags itself along',
                     '    and desire no longer is stirred.',
                     'Then people go to their eternal home',
                     '    and mourners go about the streets. ',
                     '\u2076 Remember him\u2014before the silver cord is severed,',
                     '    and the golden bowl is broken;',
                     'before the pitcher is shattered at the spring,',
                     '    and the wheel broken at the well,',
                     '\u2077 and the dust returns to the ground it came from,',
                     '    and the spirit returns to God who gave it. ',
                     '\u2078 \u201cMeaningless! Meaningless!\u201d says the Teacher.',
                     '    \u201cEverything is meaningless!\u201d ',
                     '\u2079 Not only was the Teacher wise, but he also imparted knowledge to the people. '
                     'He pondered and searched out and set in order many proverbs. '
                     '\u00b9\u2070 The Teacher searched to find just the right words, and what he wrote was '
                     'upright and true. ',
                     '\u00b9\u00b9 The words of the wise are like goads, their collected sayings like firmly '
                     'embedded nails\u2014given by one shepherd. '
                     '\u00b9\u00b2 Be warned, my son, of anything in addition to them.',
                     'Of making many books there is no end, and much study wearies the body. ',
                     '\u00b9\u00b3 Now all has been heard;',
                     '    here is the conclusion of the matter:',
                     'Fear God and keep his commandments,',
                     '    for this is the duty of all mankind.',
                     '\u00b9\u2074 For God will bring every deed into judgment,',
                     '    including every hidden thing,',
                     '    whether it is good or evil.'
                     ]
        self.assertEqual('\n'.join(eccl11_12), text, 'Passage is incorrect')

    def test_get_yaml_book(self):
        text = bible_yaml_extractor.get_yaml_book('Philemon')
        with open('./static/NIV/test_get_yaml_book.txt', 'r', encoding='utf-8') as file:
            phil = file.read()
        self.assertEqual(phil, text, 'Passage is incorrect')

    def test_get_yaml_passage_range_reverse_parameters(self):
        text = bible_yaml_extractor.get_yaml_passage_range('Ecclesiastes', 10, 1, 9, 18)
        # Chapter 10 is after chapter 9, so this should not work
        self.assertEqual('', text, 'Passage is incorrect')
        text = bible_yaml_extractor.get_yaml_passage_range('Ecclesiastes', 9, 2, 9, 1)
        # Verse 2 is after verse 1, so this should not work either
        self.assertEqual('', text, 'Passage is incorrect')

    def test_get_yaml_passage_range_negative_numbers(self):
        text = bible_yaml_extractor.get_yaml_passage_range('Ecclesiastes', 1, -1, 1, 1)
        eccl = 'The words of the Teacher, son of David, king in Jerusalem:'
        # This should apply value normalisation logic to ensure that negative values don't break the execution flow
        self.assertEqual(eccl, text, 'Passage is incorrect')
        text = bible_yaml_extractor.get_yaml_passage_range('Ecclesiastes', -1, 1, 1, 1)
        # Same normalisation should also apply for negative chapter numbers as well
        self.assertEqual(eccl, text, 'Passage is incorrect')

    def test_get_yaml_passage_range_excessive_numbers(self):
        text = bible_yaml_extractor.get_yaml_passage_range('Ecclesiastes', 9000, 1, 9000, 2)
        sample1 = ['Remember your Creator',
                   '    in the days of your youth,',
                   'before the days of trouble come',
                   '    and the years approach when you will say,',
                   '    \u201cI find no pleasure in them\u201d\u2014',
                   '\u00b2 before the sun and the light',
                   '    and the moon and the stars grow dark,',
                   '    and the clouds return after the rain;']
        # Excessive chapters should just default to the last chapter of the book
        self.assertEqual('\n'.join(sample1), text, 'Passage is incorrect')
        text = bible_yaml_extractor.get_yaml_passage_range('Ecclesiastes', 1, 9000, 1, 9001)
        sample2 = ['\u00b9\u2078 For with much wisdom comes much sorrow;',
                   '    the more knowledge, the more grief.']
        # Excessive passages should just default to the last passage of the given chapter
        self.assertEqual('\n'.join(sample2), text, 'Passage is incorrect')

    def test_get_yaml_passage_invalid(self):
        text = bible_yaml_extractor.get_yaml_passage('Barnabas', 2, 26)
        self.assertEqual('', text, 'Passage is incorrect')

    def test_get_yaml_passages_invalid(self):
        text = bible_yaml_extractor.get_yaml_passages('Barnabas', 2, 26, 27)
        self.assertEqual('', text, 'Passage is incorrect')

    def test_get_yaml_chapter_invalid(self):
        text = bible_yaml_extractor.get_yaml_chapter('Barnabas', 2)
        self.assertEqual('', text, 'Passage is incorrect')

    def test_get_yaml_chapters_invalid(self):
        text = bible_yaml_extractor.get_yaml_chapters('Barnabas', 2, 3)
        self.assertEqual('', text, 'Passage is incorrect')

    def test_get_yaml_passage_range_invalid(self):
        text = bible_yaml_extractor.get_yaml_passage_range('Barnabas', 2, 3, 2, 4)
        self.assertEqual('', text, 'Passage is incorrect')

    def test_get_yaml_passage_without_passage_numbers(self):
        text = bible_yaml_extractor.get_yaml_passage('Ecclesiastes', 2, 26, False)
        self.assertEqual('To the person who pleases him, God gives wisdom, knowledge and happiness, '
                         'but to the sinner he gives the task of gathering and storing up wealth to hand '
                         'it over to the one who pleases God. This too is meaningless, a chasing after '
                         'the wind.', text, 'Passage is incorrect')

    def test_get_yaml_passage_range_without_passage_numbers(self):
        text = bible_yaml_extractor.get_yaml_passage_range('Ecclesiastes', 9, 18, 10, 1, False)
        eccl = ['Wisdom is better than weapons of war,',
                '    but one sinner destroys much good.',
                'As dead flies give perfume a bad smell,',
                '    so a little folly outweighs wisdom and honor.'
                ]
        self.assertEqual('\n'.join(eccl), text, 'Passage is incorrect')

    def test_get_yaml_passages_without_passage_numbers(self):
        text = bible_yaml_extractor.get_yaml_passages('Ecclesiastes', 2, 24, 25, False)
        self.assertEqual('A person can do nothing better than to eat and drink and find satisfaction '
                         'in their own toil. This too, I see, is from the hand of God, '
                         'for without him, who can eat or find enjoyment?', text, 'Passage is incorrect')

    def test_get_yaml_chapter_without_passage_numbers(self):
        text = bible_yaml_extractor.get_yaml_chapter('Ecclesiastes', 11, False)
        eccl11 = ['Ship your grain across the sea;',
                  '    after many days you may receive a return.',
                  'Invest in seven ventures, yes, in eight;',
                  '    you do not know what disaster may come upon the land. ',
                  'If clouds are full of water,',
                  '    they pour rain on the earth.',
                  'Whether a tree falls to the south or to the north,',
                  '    in the place where it falls, there it will lie.',
                  'Whoever watches the wind will not plant;',
                  '    whoever looks at the clouds will not reap. ',
                  'As you do not know the path of the wind,',
                  '    or how the body is formed in a mother\u2019s womb,',
                  'so you cannot understand the work of God,',
                  '    the Maker of all things. ',
                  'Sow your seed in the morning,',
                  '    and at evening let your hands not be idle,',
                  'for you do not know which will succeed,',
                  '    whether this or that,',
                  '    or whether both will do equally well. ',
                  'Light is sweet,',
                  '    and it pleases the eyes to see the sun.',
                  'However many years anyone may live,',
                  '    let them enjoy them all.\nBut let them remember the days of darkness,',
                  '    for there will be many.',
                  '    Everything to come is meaningless. ',
                  'You who are young, be happy while you are young,',
                  '    and let your heart give you joy in the days of your youth.',
                  'Follow the ways of your heart',
                  '    and whatever your eyes see,',
                  'but know that for all these things',
                  '    God will bring you into judgment.',
                  'So then, banish anxiety from your heart',
                  '    and cast off the troubles of your body,',
                  '    for youth and vigor are meaningless.'
                  ]
        self.assertEqual('\n'.join(eccl11), text, 'Passage is incorrect')

    def test_get_yaml_chapters_without_passage_numbers(self):
        text = bible_yaml_extractor.get_yaml_chapters('Ecclesiastes', 11, 12, False)
        eccl11_12 = ['Ship your grain across the sea;',
                     '    after many days you may receive a return.',
                     'Invest in seven ventures, yes, in eight;',
                     '    you do not know what disaster may come upon the land. ',
                     'If clouds are full of water,',
                     '    they pour rain on the earth.',
                     'Whether a tree falls to the south or to the north,',
                     '    in the place where it falls, there it will lie.',
                     'Whoever watches the wind will not plant;',
                     '    whoever looks at the clouds will not reap. ',
                     'As you do not know the path of the wind,',
                     '    or how the body is formed in a mother\u2019s womb,',
                     'so you cannot understand the work of God,',
                     '    the Maker of all things. ',
                     'Sow your seed in the morning,',
                     '    and at evening let your hands not be idle,',
                     'for you do not know which will succeed,',
                     '    whether this or that,',
                     '    or whether both will do equally well. ',
                     'Light is sweet,',
                     '    and it pleases the eyes to see the sun.',
                     'However many years anyone may live,',
                     '    let them enjoy them all.\nBut let them remember the days of darkness,',
                     '    for there will be many.',
                     '    Everything to come is meaningless. ',
                     'You who are young, be happy while you are young,',
                     '    and let your heart give you joy in the days of your youth.',
                     'Follow the ways of your heart',
                     '    and whatever your eyes see,',
                     'but know that for all these things',
                     '    God will bring you into judgment.',
                     'So then, banish anxiety from your heart',
                     '    and cast off the troubles of your body,',
                     '    for youth and vigor are meaningless.',
                     # Chapter 12
                     'Remember your Creator',
                     '    in the days of your youth,',
                     'before the days of trouble come',
                     '    and the years approach when you will say,',
                     '    \u201cI find no pleasure in them\u201d\u2014',
                     'before the sun and the light',
                     '    and the moon and the stars grow dark,',
                     '    and the clouds return after the rain;',
                     'when the keepers of the house tremble,',
                     '    and the strong men stoop,',
                     'when the grinders cease because they are few,',
                     '    and those looking through the windows grow dim;',
                     'when the doors to the street are closed',
                     '    and the sound of grinding fades;',
                     'when people rise up at the sound of birds,',
                     '    but all their songs grow faint;',
                     'when people are afraid of heights',
                     '    and of dangers in the streets;',
                     'when the almond tree blossoms',
                     '    and the grasshopper drags itself along',
                     '    and desire no longer is stirred.',
                     'Then people go to their eternal home',
                     '    and mourners go about the streets. ',
                     'Remember him\u2014before the silver cord is severed,',
                     '    and the golden bowl is broken;',
                     'before the pitcher is shattered at the spring,',
                     '    and the wheel broken at the well,',
                     'and the dust returns to the ground it came from,',
                     '    and the spirit returns to God who gave it. ',
                     '\u201cMeaningless! Meaningless!\u201d says the Teacher.',
                     '    \u201cEverything is meaningless!\u201d ',
                     'Not only was the Teacher wise, but he also imparted knowledge to the people. '
                     'He pondered and searched out and set in order many proverbs. '
                     'The Teacher searched to find just the right words, and what he wrote was '
                     'upright and true. ',
                     'The words of the wise are like goads, their collected sayings like firmly '
                     'embedded nails\u2014given by one shepherd. '
                     'Be warned, my son, of anything in addition to them.',
                     'Of making many books there is no end, and much study wearies the body. ',
                     'Now all has been heard;',
                     '    here is the conclusion of the matter:',
                     'Fear God and keep his commandments,',
                     '    for this is the duty of all mankind.',
                     'For God will bring every deed into judgment,',
                     '    including every hidden thing,',
                     '    whether it is good or evil.'
                     ]
        self.assertEqual('\n'.join(eccl11_12), text, 'Passage is incorrect')

    def test_get_yaml_passage_nlt(self):
        text = bible_yaml_extractor.get_yaml_passage('Ecclesiastes', 2, 26, translation='NLT')
        self.assertEqual('\u00b2\u2076 God gives wisdom, knowledge, and joy to those who please him. But if a '
                         'sinner becomes wealthy, God takes the wealth away and gives it to those who '
                         'please him. This, too, is meaningless\u2014like chasing the wind.', text,
                         'Passage is incorrect')

    def test_get_yaml_passage_invalid_translation(self):
        text = bible_yaml_extractor.get_yaml_passage('Ecclesiastes', 2, 26, translation='LOL')
        self.assertEqual('', text, 'Passage is incorrect')

if __name__ == "__main__":
    unittest.main()
