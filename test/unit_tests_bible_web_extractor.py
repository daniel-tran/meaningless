import unittest
import sys
sys.path.append('../')
from meaningless import WebExtractor, InvalidSearchError, UnsupportedTranslationError


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def test_get_passage(self):
        bible = WebExtractor()
        text = bible.search('Ecclesiastes 1:17')
        self.assertEqual('\u00b9\u2077 Then I applied myself to the understanding of wisdom, and also of '
                         'madness and folly, but I learned that this, too, is a chasing after the wind.', text,
                         'Passage is incorrect')

    def test_get_passage_empty(self):
        bible = WebExtractor()
        self.assertRaises(InvalidSearchError, bible.search, '')

    def test_get_passage_invalid(self):
        bible = WebExtractor()
        self.assertRaises(InvalidSearchError, bible.search, 'Barnabas 7')

    def test_get_passage_in_table_form(self):
        bible = WebExtractor()
        text = bible.search('Nehemiah 7:30 - 31')
        self.assertEqual('\u00b3\u2070 of Ramah and Geba 621 \u00b3\u00b9 of Mikmash 122', text,
                         'Passage is incorrect')

    def test_get_passage_with_footnotes(self):
        bible = WebExtractor()
        text = bible.search('Nehemiah 7:71')
        # Footnotes are to be ignored
        self.assertEqual('\u2077\u00b9 Some of the heads of the families gave to the treasury '
                         'for the work 20,000 darics of gold and 2,200 minas of silver.', text,
                         'Passage is incorrect')

    def test_get_passage_with_italics_and_unicode_quotation_marks(self):
        bible = WebExtractor()
        text = bible.search('Matthew 27:46')
        # Preserve Unicode quotation marks, and don't bother trying to carry over the italics styling.
        self.assertEqual('\u2074\u2076 About three in the afternoon Jesus cried out in a loud voice, '
                         '\u201cEli, Eli, lema sabachthani?\u201d (which means \u201cMy God, my God, '
                         'why have you forsaken me?\u201d).',
                         text, 'Passage is incorrect')

    def test_get_passage_with_headings(self):
        bible = WebExtractor()
        text = bible.search('Exodus 22:31-23:1')
        ex22 = '\u00b3\u00b9 \u201cYou are to be my holy people. So do not eat the meat of an animal ' \
               'torn by wild beasts; throw it to the dogs. '
        ex23 = '\u201cDo not spread false reports. Do not help a guilty person by being a malicious witness.'
        # Use a multi-line string to account for the chapter transition
        self.assertEqual('''{0}\n\n{1}'''.format(ex22, ex23), text, 'Passage is incorrect')

    def test_get_passage_with_subheadings(self):
        bible = WebExtractor()
        text = bible.search('Ezekiel 40:19-20')
        ez40_19 = '\u00b9\u2079 Then he measured the distance from the inside of the lower gateway to ' \
                  'the outside of the inner court; it was a hundred cubits on the east side as well as on the north. '
        ez40_20 = '\u00b2\u2070 Then he measured the length and width of the north gate, ' \
                  'leading into the outer court.'
        # Ignore the subheading, but start its paragraph contents on a new line
        self.assertEqual('''{0}\n{1}'''.format(ez40_19, ez40_20), text, 'Passage is incorrect')

    def test_get_passage_with_indentations(self):
        bible = WebExtractor()
        text = bible.search('Ecclesiastes 1:3')
        ecc1_3 = ['\u00b3 What do people gain from all their labors',
                  '    at which they toil under the sun?'
                  ]
        # Preserve leading spaces in the second line of the passage
        self.assertEqual('\n'.join(ecc1_3), text, 'Passage is incorrect')

    def test_get_passage_with_extended_dash(self):
        bible = WebExtractor()
        text = bible.search('Psalms 42:6')
        psalm_6 = ['\u2076 My soul is downcast within me;',
                   '    therefore I will remember you',
                   'from the land of the Jordan,',
                   '    the heights of Hermon\u2014from Mount Mizar.'
                   ]
        # The extended dash is a Unicode character, and should be preserved
        self.assertEqual('\n'.join(psalm_6), text, 'Passage is incorrect')

    def test_get_passage_with_spaced_out_passage_details(self):
        bible = WebExtractor()
        text = bible.search('  Titus                       2                 :                     1  ')
        titus2_1 = 'You, however, must teach what is appropriate to sound doctrine.'
        # The Bible Gateway search engine currently removes superfluous spaces in the passage string
        self.assertEqual(titus2_1, text, 'Passage is incorrect')

    def test_get_passage_with_dual_unicode_quotation_marks(self):
        bible = WebExtractor()
        text = bible.search('Leviticus 15:12')
        lev15_12 = '\u00b9\u00b2 \u201c\u2018A clay pot that the man touches must be broken,' \
                   ' and any wooden article is to be rinsed with water.'
        # Preserve both sets of Unicode quotation marks
        self.assertEqual(lev15_12, text, 'Passage is incorrect')

    def test_get_passage_with_poetry_indentation(self):
        bible = WebExtractor()
        text = bible.search('Deuteronomy 7:10')
        deut7_10 = ['\u00b9\u2070 But',
                    'those who hate him he will repay to their face by destruction;',
                    '    he will not be slow to repay to their face those who hate him.']
        # In some cases, passage sections are nested within another <div> tag, presumably to apply CSS indentation
        self.assertEqual('\n'.join(deut7_10), text, 'Passage is incorrect')

    def test_get_passage_with_max_passage_limitation(self):
        bible = WebExtractor()
        text = bible.search('Genesis 1:1 - 40:38')
        gen10_15 = ['\u00b9\u2075 Canaan was the father of',
                    'Sidon his firstborn, and of the Hittites,']
        # The Bible Gateway search engine has a certain limit on the number of passages that can be requested at once.
        # Not much is currently known about this limitation, but users should be aware of this during use.
        # In this particular case, the last verse to return should be Genesis 10:15
        self.assertTrue(text.endswith('\n'.join(gen10_15)), 'Passage is incorrect')

    def test_get_empty_passage(self):
        bible = WebExtractor()
        text = bible.search('Luke 17:36')
        luke17_36 = '\u00b3\u2076'
        # In rare cases, the passage can be empty/non-existent depending on the particular translation used.
        # For NIV, this passage is left empty, but ESV outright omits the passage.
        self.assertEqual(luke17_36, text, 'Passage is incorrect')

    def test_get_empty_passage_midway(self):
        bible = WebExtractor()
        text = bible.search('Luke 23:16 - 18')
        luke17 = ['\u00b9\u2076 Therefore, I will punish him and then release him.\u201d \u00b9\u2077  ',
                  '\u00b9\u2078 But the whole crowd shouted, \u201cAway with this man! Release Barabbas to us!\u201d'
                  ]
        # An empty passage in the middle of two other passages preserves its spaces
        self.assertEqual('\n'.join(luke17), text, 'Passage is incorrect')

    def test_get_passage_with_passage_separator(self):
        bible = WebExtractor(passage_separator='\n\n')
        text = bible.search('3 John 1:3 - 4')
        john = ['\u00b3 It gave me great joy when some believers came and testified about your faithfulness to the '
                'truth, telling how you continue to walk in it. ',
                '\u2074 I have no greater joy than to hear that my children are walking in the truth.']
        # These two passages continue on the same line, but the separator should force them onto new lines
        self.assertEqual('\n\n'.join(john), text, 'Passage is incorrect')

    def test_get_passage_without_passage_numbers(self):
        bible = WebExtractor(show_passage_numbers=False)
        text = bible.search('2 John 1:2')
        john = 'because of the truth, which lives in us and will be with us forever:'
        self.assertEqual(john, text, 'Passage is incorrect')

    def test_get_passage_with_passage_separator_without_passage_numbers(self):
        bible = WebExtractor(passage_separator='\n\n', show_passage_numbers=False)
        text = bible.search('Jude 1:22 - 23')
        jude1 = ['Be merciful to those who doubt; ',
                 'save others by snatching them from the fire; to others show mercy, '
                 'mixed with fear\u2014hating even the clothing stained by corrupted flesh.']
        self.assertEqual('\n\n'.join(jude1), text, 'Passage is incorrect')

    def test_get_empty_passage_without_passage_numbers(self):
        bible = WebExtractor(show_passage_numbers=False)
        text = bible.search('Luke 17:36')
        luke17_36 = ''
        # Without the passage number, the resulting passage text is empty even though the passage is "valid"
        self.assertEqual(luke17_36, text, 'Passage is incorrect')

    def test_get_passage_unsupported_translation(self):
        bible = WebExtractor(translation='mounce')
        self.assertRaises(UnsupportedTranslationError, bible.search, 'Song of Songs 1:4')

    def test_get_passage_nlt(self):
        bible = WebExtractor(translation='NLT')
        text = bible.search('Ecclesiastes 1:17')
        eccl1_17 = '\u00b9\u2077 So I set out to learn everything from wisdom to madness and folly. ' \
                   'But I learned firsthand that pursuing all this is like chasing the wind.'
        self.assertEqual(eccl1_17, text, 'Passage is incorrect')

    def test_get_passage_nlt_interlude(self):
        bible = WebExtractor(translation='NLT')
        text = bible.search('Psalm 32:4')
        psalm32_4 = ['\u2074 Day and night your hand of discipline was heavy on me.',
                     '    My strength evaporated like water in the summer heat.']
        # Explicit interludes should be omitted, and usually show as italicised text in the Psalm.
        # Implicit interludes are embedded within the passage itself, so not much can be done about it (e.g. YLT)
        self.assertEqual('\n'.join(psalm32_4), text, 'Passage is incorrect')

    def test_get_passage_esv_translation_note(self):
        bible = WebExtractor(translation='ESV')
        text = bible.search('John 7:53')
        john7_53 = '\u2075\u00b3 [[They went each to his own house,'
        # Translation notes can vary between translations in both content and tag representation.
        # This could be problematic depending on how many form variations are present on the Bible Gateway site.
        self.assertEqual(john7_53, text, 'Passage is incorrect')

    def test_get_passage_lowercase_translation(self):
        bible = WebExtractor(translation='NLT')
        passage = 'Ecclesiastes 1:17'
        text1 = bible.search(passage)
        bible.translation = 'nlt'
        text2 = bible.search(passage)
        # Translations should be case insensitive under the hood
        self.assertEqual(text1, text2, 'Passages do not match')

    def test_get_passage_nasb_asterisk(self):
        bible = WebExtractor(translation='NASB')
        text = bible.search('John 5:8')
        john5_8 = '\u2078 Jesus said to him, \u201cGet up, pick up your pallet and walk.\u201d'
        # An asterisk is normally present within this passage using this translation, but it should be omitted.
        self.assertEqual(john5_8, text, 'Passage is incorrect')

    # -------------- Tests for the alternative interfaces --------------
    # Given the precondition that directly querying the Bible Gateway site has been tested extensively,
    # these tests are only concerned with ensuring method consistency with the same data.

    @staticmethod
    def get_alternative_interface_options():
        return [{'translation': 'NIV', 'show_passage_numbers': True, 'passage_separator': ''},
                {'translation': 'NLT', 'show_passage_numbers': True, 'passage_separator': ''},
                {'translation': 'NIV', 'show_passage_numbers': False, 'passage_separator': ''},
                {'translation': 'NIV', 'show_passage_numbers': True, 'passage_separator': '\n'},
                ]

    def test_get_online_passage(self):
        bible = WebExtractor()
        options = self.get_alternative_interface_options()
        for option in options:
            bible.translation = option['translation']
            bible.show_passage_numbers = option['show_passage_numbers']
            bible.passage_separator = option['passage_separator']

            text1 = bible.search('Ecclesiastes 1:17')
            text2 = bible.get_passage('Ecclesiastes', 1, 17)
            self.assertEqual(text1, text2, 'Passage is incorrect')

    def test_get_online_passages(self):
        bible = WebExtractor()
        options = self.get_alternative_interface_options()
        for option in options:
            bible.translation = option['translation']
            bible.show_passage_numbers = option['show_passage_numbers']
            bible.passage_separator = option['passage_separator']

            text1 = bible.search('Ezekiel 40:19-20')
            text2 = bible.get_passages('Ezekiel', 40, 19, 20)
            self.assertEqual(text1, text2, 'Passage is incorrect')

    def test_get_online_chapter(self):
        bible = WebExtractor()
        options = self.get_alternative_interface_options()
        for option in options:
            bible.translation = option['translation']
            bible.show_passage_numbers = option['show_passage_numbers']
            bible.passage_separator = option['passage_separator']

            text1 = bible.search('Daniel 5')
            text2 = bible.get_chapter('Daniel', 5)
            self.assertEqual(text1, text2, 'Passage is incorrect')

    def test_get_online_chapters(self):
        bible = WebExtractor()
        options = self.get_alternative_interface_options()
        for option in options:
            bible.translation = option['translation']
            bible.show_passage_numbers = option['show_passage_numbers']

            text1 = bible.get_chapter('Amos', 8) + '\n' + bible.get_chapter('Amos', 9)
            text2 = bible.get_chapters('Amos', 8, 9)
            # Chapters interface should be the same as requesting the individual chapters with newline separators
            self.assertEqual(text1, text2, 'Passage is incorrect')

    def test_get_online_passage_range(self):
        bible = WebExtractor()
        options = self.get_alternative_interface_options()
        for option in options:
            bible.translation = option['translation']
            bible.show_passage_numbers = option['show_passage_numbers']

            text1 = bible.get_passage('Amos', 8, 14) + '\n' + bible.get_passage('Amos', 9, 1)
            text2 = bible.get_passage_range('Amos', 8, 14, 9, 1)
            # A passage range should be the same as putting all the passage together with newline separators
            self.assertEqual(text1, text2, 'Passage is incorrect')

    def test_get_online_book(self):
        bible = WebExtractor()
        options = self.get_alternative_interface_options()
        for option in options:
            bible.translation = option['translation']
            bible.show_passage_numbers = option['show_passage_numbers']

            text1 = bible.get_chapters('2 Thessalonians', 1, 3)
            text2 = bible.get_book('2 Thessalonians')
            # A book should be the same ass getting all the chapters in a given book
            self.assertEqual(text1, text2, 'Passage is incorrect')

    def test_get_online_passage_range_with_intermediate_chapters(self):
        bible = WebExtractor()
        text1 = bible.get_passage('Daniel', 3, 30) + '\n' + \
            bible.get_chapter('Daniel', 4) + '\n' + \
            bible.get_passage('Daniel', 5, 1)
        text2 = bible.get_passage_range('Daniel', 3, 30, 5, 1)
        # A passage range with intermediate chapters should be the same as manually putting all the passages together
        self.assertEqual(text1, text2, 'Passage is incorrect')

    def test_get_online_passage_range_from_same_chapter(self):
        bible = WebExtractor()
        text1 = bible.get_passages('Ezekiel', 40, 19, 20)
        # A passage range in the same chapter should be the same as calling the passages extraction method
        text2 = bible.get_passage_range('Ezekiel', 40, 19, 40, 20)
        self.assertEqual(text1, text2, 'Passage is incorrect')

    def test_get_online_passage_with_excessive_values(self):
        bible = WebExtractor()
        text1 = bible.search('Ecclesiastes 1:1')
        text2 = bible.get_passage('Ecclesiastes', -1, -1)
        self.assertEqual(text1, text2, 'Passage is incorrect')
        # Starting passage is not valid
        self.assertRaises(InvalidSearchError, bible.get_passage, 'Ecclesiastes', 1000, 1000)

    def test_get_online_passages_with_excessive_values(self):
        bible = WebExtractor()
        text1 = bible.search('Ecclesiastes 1:1')
        text2 = bible.get_passages('Ecclesiastes', -1, -1, -1)
        self.assertEqual(text1, text2, 'Passage is incorrect')
        # Starting passage is not valid
        self.assertRaises(InvalidSearchError, bible.get_passages, 'Ecclesiastes', 1000, 1000, 1000)
        # Starting passage is valid again
        text1 = bible.search('Ecclesiastes 12')
        text2 = bible.get_passages('Ecclesiastes', 1000, 1, 1000)
        self.assertEqual(text1, text2, 'Passage is incorrect')

    def test_get_online_chapter_with_excessive_values(self):
        bible = WebExtractor()
        text1 = bible.search('Ecclesiastes 1')
        text2 = bible.get_chapter('Ecclesiastes', -1)
        self.assertEqual(text1, text2, 'Passage is incorrect')
        # This should scale down to the last chapter number of the book
        text1 = bible.search('Ecclesiastes 12')
        text2 = bible.get_chapter('Ecclesiastes', 1000)
        self.assertEqual(text1, text2, 'Passage is incorrect')

    def test_get_online_chapters_with_excessive_values(self):
        bible = WebExtractor()
        text1 = bible.search('Ecclesiastes 1')
        text2 = bible.get_chapters('Ecclesiastes', -1, -1)
        self.assertEqual(text1, text2, 'Passage is incorrect')
        # This should scale down to the last chapter number of the book
        text1 = bible.search('Ecclesiastes 12')
        text2 = bible.get_chapters('Ecclesiastes', 1000, 1000)
        self.assertEqual(text1, text2, 'Passage is incorrect')

    def test_get_online_passage_range_with_excessive_values(self):
        bible = WebExtractor()
        text1 = bible.search('Ecclesiastes 1:1')
        text2 = bible.get_passage_range('Ecclesiastes', -1, -1, -1, -1)
        self.assertEqual(text1, text2, 'Passage is incorrect')
        # Starting passage is not valid
        self.assertRaises(InvalidSearchError, bible.get_passage_range, 'Ecclesiastes', 1000, 1000, 1000, 1000)
        # Starting passage is valid again
        text1 = bible.search('Ecclesiastes 12')
        text2 = bible.get_passage_range('Ecclesiastes', 1000, -1, 1000, 1000)
        self.assertEqual(text1, text2, 'Passage is incorrect')

    # -------------- Tests which are ignored due to being unsupported translations --------------

    # def test_get_passage_exb(self):
    #     text = bible_extractor.get_passage('Ecclesiastes 1:17', translation='EXB')
    #     eccl1_17 = '\u00b9\u2077 So I \u00b7decided to find out about wisdom and knowledge and also ' \
    #                '\u00b7about foolish thinking, but this turned out to be like chasing the wind.'
    #     # The in-line notes should be removed along with any erroneous spaces
    #     self.assertEqual(eccl1_17, text, 'Passage is incorrect')

    # def test_get_passage_hcsb_interlude(self):
    #     text = bible_extractor.get_passage('Psalm 32:4', translation='HCSB')
    #     psalm32_4 = ['\u2074 For day and night Your hand was heavy on me;',
    #                  'my strength was drained',
    #                  'as in the summer\u2019s heat.']
    #     # Some translations such as HCSB use a dedicated <selah> tag for Psalm interludes, and is to be excluded
    #     # as it does not appear to be part of the actual Psalm lyrics.
    #     self.assertEqual('\n'.join(psalm32_4), text, 'Passage is incorrect')

if __name__ == "__main__":
    unittest.main()
