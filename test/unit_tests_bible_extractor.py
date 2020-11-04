import unittest
import sys
sys.path.append('../src/')
from meaningless import bible_extractor


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def test_get_passage(self):
        text = bible_extractor.get_passage('Ecclesiastes 1:17')
        self.assertEqual('\u00b9\u2077 Then I applied myself to the understanding of wisdom, and also of '
                         'madness and folly, but I learned that this, too, is a chasing after the wind.', text,
                         'Passage is incorrect')

    def test_get_passage_empty(self):
        text = bible_extractor.get_passage('')
        self.assertEqual('', text, 'Empty passage should result in an empty string')

    def test_get_passage_invalid(self):
        text = bible_extractor.get_passage('Barnabas 7')
        self.assertEqual('', text, 'Invalid passage should result in an empty string')

    def test_get_passage_in_table_form(self):
        text = bible_extractor.get_passage('Nehemiah 7:30 - 31')
        self.assertEqual('\u00b3\u2070 of Ramah and Geba 621 \u00b3\u00b9 of Mikmash 122', text,
                         'Passage is incorrect')

    def test_get_passage_with_footnotes(self):
        text = bible_extractor.get_passage('Nehemiah 7:71')
        # Footnotes are to be ignored
        self.assertEqual('\u2077\u00b9 Some of the heads of the families gave to the treasury '
                         'for the work 20,000 darics of gold and 2,200 minas of silver.', text,
                         'Passage is incorrect')

    def test_get_passage_with_italics_and_unicode_quotation_marks(self):
        text = bible_extractor.get_passage('Matthew 27:46')
        # Preserve Unicode quotation marks, and don't bother trying to carry over the italics styling.
        self.assertEqual('\u2074\u2076 About three in the afternoon Jesus cried out in a loud voice, '
                         '\u201cEli, Eli, lema sabachthani?\u201d (which means \u201cMy God, my God, '
                         'why have you forsaken me?\u201d).',
                         text, 'Passage is incorrect')

    def test_get_passage_with_headings(self):
        text = bible_extractor.get_passage('Exodus 22:31-23:1')
        ex22 = '\u00b3\u00b9 \u201cYou are to be my holy people. So do not eat the meat of an animal ' \
               'torn by wild beasts; throw it to the dogs. '
        ex23 = '\u201cDo not spread false reports. Do not help a guilty person by being a malicious witness.'
        # Use a multi-line string to account for the chapter transition
        self.assertEqual('''{0}

{1}'''.format(ex22, ex23), text, 'Passage is incorrect')

    def test_get_passage_with_subheadings(self):
        text = bible_extractor.get_passage('Ezekiel 40:19-20')
        ez40_19 = '\u00b9\u2079 Then he measured the distance from the inside of the lower gateway to ' \
                  'the outside of the inner court; it was a hundred cubits on the east side as well as on the north. '
        ez40_20 = '\u00b2\u2070 Then he measured the length and width of the north gate, ' \
                  'leading into the outer court.'
        # Ignore the subheading, but start its paragraph contents on a new line
        self.assertEqual('''{0}
{1}'''.format(ez40_19, ez40_20), text, 'Passage is incorrect')

    def test_get_passage_with_indentations(self):
        text = bible_extractor.get_passage('Ecclesiastes 1:3')
        ecc1_3 = ['\u00b3 What do people gain from all their labors',
                  '    at which they toil under the sun?'
                  ]
        # Preserve leading spaces in the second line of the passage
        self.assertEqual('\n'.join(ecc1_3), text, 'Passage is incorrect')

    def test_get_passage_with_extended_dash(self):
        text = bible_extractor.get_passage('Psalms 42:6')
        psalm_6 = ['\u2076 My soul is downcast within me;',
                   '    therefore I will remember you',
                   'from the land of the Jordan,',
                   '    the heights of Hermon—from Mount Mizar.'
                   ]
        # The extended dash is a Unicode character, and should be preserved
        self.assertEqual('\n'.join(psalm_6), text, 'Passage is incorrect')

    def test_get_passage_with_spaced_out_passage_details(self):
        text = bible_extractor.get_passage('  Titus                       2                 :                     1  ')
        titus2_1 = 'You, however, must teach what is appropriate to sound doctrine.'
        # The Bible Gateway search engine currently removes superfluous spaces in the passage string
        self.assertEqual(titus2_1, text, 'Passage is incorrect')

    def test_get_passage_with_dual_unicode_quotation_marks(self):
        text = bible_extractor.get_passage('Leviticus 15:12')
        lev15_12 = '\u00b9\u00b2 \u201c\u2018A clay pot that the man touches must be broken,' \
                   ' and any wooden article is to be rinsed with water.'
        # Preserve both sets of Unicode quotation marks
        self.assertEqual(lev15_12, text, 'Passage is incorrect')

    def test_get_passage_with_poetry_indentation(self):
        text = bible_extractor.get_passage('Deuteronomy 7:10')
        deut7_10 = ['\u00b9\u2070 But',
                    'those who hate him he will repay to their face by destruction;',
                    '    he will not be slow to repay to their face those who hate him.']
        # In some cases, passage sections are nested within another <div> tag, presumably to apply CSS indentation
        self.assertEqual('\n'.join(deut7_10), text, 'Passage is incorrect')

    def test_get_passage_with_max_passage_limitation(self):
        text = bible_extractor.get_passage('Genesis 1:1 - 40:38')
        gen10_15 = ['\u00b9\u2075 Canaan was the father of',
                    'Sidon his firstborn, and of the Hittites,']
        # The Bible Gateway search engine has a certain limit on the number of passages that can be requested at once.
        # Not much is currently known about this limitation, but users should be aware of this during use.
        # In this particular case, the last verse to return should be Genesis 10:15
        self.assertTrue(text.endswith('\n'.join(gen10_15)), 'Passage is incorrect')


if __name__ == "__main__":
    unittest.main()
