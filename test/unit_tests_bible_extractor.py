import unittest
import sys
sys.path.append('../src/')
from meaningless import bible_extractor


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def test_get_passage(self):
        text = bible_extractor.get_passage('Ecclesiastes 1:17')
        self.assertEqual('\u00b9\u2077\xa0Then I applied myself to the understanding of wisdom, and also of '
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
        self.assertEqual('\u00b3\u2070\xa0of Ramah and Geba 621 \u00b3\u00b9\xa0of Mikmash 122', text,
                         'Passage is incorrect')

    def test_get_passage_with_footnotes(self):
        text = bible_extractor.get_passage('Nehemiah 7:71')
        # Footnotes are to be ignored
        self.assertEqual('\u2077\u00b9\xa0Some of the heads of the families gave to the treasury '
                         'for the work 20,000 darics of gold and 2,200 minas of silver.', text,
                         'Passage is incorrect')

    def test_get_passage_with_italics_and_unicode_quotation_marks(self):
        text = bible_extractor.get_passage('Matthew 27:46')
        # Preserve Unicode quotation marks, and don't bother trying to carry over the italics styling.
        self.assertEqual('\u2074\u2076\xa0About three in the afternoon Jesus cried out in a loud voice, '
                         '\u201cEli, Eli, lema sabachthani?\u201d (which means \u201cMy God, my God, '
                         'why have you forsaken me?\u201d).',
                         text, 'Passage is incorrect')

    def test_get_passage_with_headings(self):
        text = bible_extractor.get_passage('Exodus 22:31-23:1')
        ex22 = '\u00b3\u00b9\xa0\u201cYou are to be my holy people. So do not eat the meat of an animal ' \
               'torn by wild beasts; throw it to the dogs. '
        ex23 = '\u201cDo not spread false reports. Do not help a guilty person by being a malicious witness.'
        # Use a multi-line string to account for the chapter transition
        self.assertEqual('''{0}

{1}'''.format(ex22, ex23), text, 'Passage is incorrect')

    def test_get_passage_with_subheadings(self):
        text = bible_extractor.get_passage('Ezekiel 40:19-20')
        ez40_19 = '\u00b9\u2079\xa0Then he measured the distance from the inside of the lower gateway to ' \
                  'the outside of the inner court; it was a hundred cubits on the east side as well as on the north. '
        ez40_20 = '\u00b2\u2070\xa0Then he measured the length and width of the north gate, ' \
                  'leading into the outer court.'
        # Ignore the subheading, but start its paragraph contents on a new line
        self.assertEqual('''{0}
{1}'''.format(ez40_19, ez40_20), text, 'Passage is incorrect')


if __name__ == "__main__":
    unittest.main()
