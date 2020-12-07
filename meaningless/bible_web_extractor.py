from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlencode
import re
from meaningless.utilities import common
from meaningless.utilities.exceptions import InvalidSearchError, UnsupportedTranslationError


class WebExtractor:

    def __init__(self, translation='NIV', show_passage_numbers=True, output_as_list=False,
                 strip_excess_whitespace_from_list=False, passage_separator=''):
        """
        :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
        :param show_passage_numbers: If True, any present passage numbers are preserved.
        :param output_as_list: When True, returns the passage data as a list of strings.
        :param strip_excess_whitespace_from_list: When True and output_as_list is also True, leading and trailing
                                                  whitespace characters are removed for each string element in the list.
        :param passage_separator: An optional string added to the front of a passage (placed before the passage number).
        """
        self.translation = translation
        self.show_passage_numbers = show_passage_numbers
        self.output_as_list = output_as_list
        self.strip_excess_whitespace_from_list = strip_excess_whitespace_from_list
        self.passage_separator = passage_separator

    def get_passage(self, book, chapter, passage):
        """
        Gets a single passage from the Bible Gateway site
        :param book: Name of the book
        :param chapter: Chapter number
        :param passage: Passage number
        :return: The specified passage. Empty string/list if the passage is invalid.
        """
        # Capping the chapter and passage information, as this gets included in site search string and can cause
        # the web request to stagger if this manages to be long enough.
        capped_chapter = common.get_capped_integer(chapter, max_value=common.get_chapter_count(book, self.translation))
        capped_passage = common.get_capped_integer(passage)
        return self.search('{0} {1}:{2}'.format(book, capped_chapter, capped_passage))

    def get_passages(self, book, chapter, passage_from, passage_to):
        """
        Gets a range of passages of the same chapter from the Bible Gateway site
        :param book: Name of the book
        :param chapter: Chapter number
        :param passage_from: First passage number to get
        :param passage_to: Last passage number to get
        :return: The passages between the specified passages (inclusive). Empty string/list if the passage is invalid.
        """
        # Capping the chapter and passage information, as this gets included in site search string and can cause
        # the web request to stagger if this manages to be long enough.
        capped_chapter = common.get_capped_integer(chapter, max_value=common.get_chapter_count(book, self.translation))
        capped_passage_from = common.get_capped_integer(passage_from)
        capped_passage_to = common.get_capped_integer(passage_to)
        return self.search('{0} {1}:{2} - {3}'.format(book, capped_chapter, capped_passage_from, capped_passage_to))

    def get_chapter(self, book, chapter):
        """
        Gets a single chapter from the Bible Gateway site
        :param book: Name of the book
        :param chapter: Chapter number
        :return: All passages in the chapter. Empty string/list if the passage is invalid.
        """
        # Capping the chapter information, as this gets included in site search string and can cause
        # the web request to stagger if this manages to be long enough.
        capped_chapter = common.get_capped_integer(chapter, max_value=common.get_chapter_count(book, self.translation))
        return self.search('{0} {1}'.format(book, capped_chapter))

    def get_chapters(self, book, chapter_from, chapter_to):
        """
        Gets a range of passages from a specified chapters selection from the Bible Gateway site
        :param book: Name of the book
        :param chapter_from: First chapter number to get
        :param chapter_to: Last chapter number to get
        :return: All passages between the specified chapters (inclusive). Empty string/list if the passage is invalid.
        """
        # Capping the chapter information, as this gets included in site search string and can cause
        # the web request to stagger if this manages to be long enough.
        capped_chapter_from = common.get_capped_integer(chapter_from,
                                                        max_value=common.get_chapter_count(book, self.translation))
        capped_chapter_to = common.get_capped_integer(chapter_to,
                                                      max_value=common.get_chapter_count(book, self.translation))
        # Retrieve chapters one by one to stay within the max. text limit when requesting for passages.
        # Add 1 to the end of the range, since the last chapter is also to be included.
        chapters = [self.get_chapter(book, chapter) for chapter in range(capped_chapter_from, capped_chapter_to + 1)]
        if self.output_as_list:
            # Flattens the data structure from a list of lists to a normal list
            return [chapter for chapter_list in chapters for chapter in chapter_list]
        return '\n'.join(chapters)

    def get_book(self, book):
        """
        Gets all chapters for a specific book from the Bible Gateway site
        :param book: Name of the book
        :return: All passages in the specified book. Empty string/list if the passage is invalid.
        """
        return self.get_chapters(book, 1, common.get_chapter_count(book, self.translation))

    def get_passage_range(self, book, chapter_from, passage_from, chapter_to, passage_to):
        """
        Gets a range of passages from one specific passage to another passage from the Bible Gateway site
        :param book: Name of the book
        :param chapter_from: First chapter number to get
        :param passage_from: First passage number to get in the first chapter
        :param chapter_to: Last chapter number to get
        :param passage_to: Last passage number to get in the last chapter
        :return: All passages between the specified passages (inclusive). Empty string/list if the passage is invalid.
        """
        # Capping the chapter and passage information, as this gets included in site search string and can cause
        # the web request to stagger if this manages to be long enough.
        capped_chapter_from = common.get_capped_integer(chapter_from,
                                                        max_value=common.get_chapter_count(book, self.translation))
        capped_passage_from = common.get_capped_integer(passage_from)
        capped_chapter_to = common.get_capped_integer(chapter_to,
                                                      max_value=common.get_chapter_count(book, self.translation))
        capped_passage_to = common.get_capped_integer(passage_to)
        # Defer to a simpler alternative function when sourcing passages from the same chapter
        if capped_chapter_from == capped_chapter_to:
            return self.get_passages(book, capped_chapter_from, capped_passage_from, capped_passage_to)

        # Get the partial section of the first chapter being requested, omitting some initial passages
        initial_chapter = self.get_passages(book, capped_chapter_from, capped_passage_from, common.get_end_of_chapter())
        # Get the partial section of the last chapter being requested, omitting some trailing passages
        final_chapter = self.get_passages(book, capped_chapter_to, 1, capped_passage_to)
        # Get all the chapters in between the initial and final chapters (exclusive since they have been pre-fetched).
        # Sandwich those chapters between the first and last pre-fetched chapters to combine all the passage data.
        chapters = [initial_chapter] + \
                   [self.get_chapter(book, chapter)
                    for chapter in range(capped_chapter_from + 1, capped_chapter_to)] + [final_chapter]
        if self.output_as_list:
            # Flattens the data structure from a list of lists to a normal list
            return [chapter for chapter_list in chapters for chapter in chapter_list]
        return '\n'.join(chapters)

    def search(self, passage_name):
        """
        Retrieves a specific passage or set of passages directly from the Bible Gateway site
        :param passage_name: Name of the Bible passage which is valid when used on www.biblegateway.com
        :return: Bible passage with preserved line breaks
        """
        # Some translations are very tricky to extract passages from, and currently, so specific extraction logic
        # for these translations should not be introduced until they need to be supported.
        translation = self.translation.upper()
        if common.is_unsupported_translation(translation):
            raise UnsupportedTranslationError(translation)

        # Use the printer-friendly view since there are fewer page elements to load and process
        source_site_params = urlencode({'version': self.translation, 'search': passage_name, 'interface': 'print'})
        source_site = 'https://www.biblegateway.com/passage/?{0}'.format(source_site_params)
        soup = BeautifulSoup(common.get_page(source_site), 'html.parser')

        # Don't collect contents from an invalid verse, since they do not exist.
        # A fail-fast approach can be taken by checking for certain indicators of invalidity.
        if not soup.find('div', {'class': 'passage-content'}):
            raise InvalidSearchError(passage_name, self.translation)

        # To get a list, the passage separator is given an actual practical use as an indicator of where to split
        # the string to create list elements.
        temp_passage_separator = self.passage_separator
        if self.output_as_list:
            self.passage_separator = '-_-'

        # Compile the list of tags to remove from the parsed web page, corresponding to the following elements:
        # h1
        #    - Ignore passage display
        # h3
        #    - Ignore section headings
        # h4
        #    - Ignore subsection headings, such as those in Ezekiel 40
        # a with 'full-chap-link' class
        #    - Ignore the "Read Full Chapter" text, which is carefully embedded within the passage
        # sup with 'crossreference' class
        #    - Ignore cross references
        # sup with 'footnote' class
        #    - Ignore in-line footnotes
        # div with one of the 'footnotes', 'dropdowns', 'crossrefs', 'passage-other-trans' classes
        #    - Ignore the footer area, which is composed of several main tags
        # span with 'selah' class
        #    - Ignore explicit Psalm interludes in the translations such as NLT and CEB
        # selah
        #    - Ignore explicit Psalm interludes in the translations such as HCSB
        # p with 'translation-note' class
        #    - Ignore explicit translation notes in translations such as ESV
        removable_tags = soup.find_all(re.compile('^h1$|^h3$|^h4$')) \
            + soup.find_all('a', {'class': 'full-chap-link'}) \
            + soup.find_all('sup', {'class': re.compile('^crossreference$|^footnote$')}) \
            + soup.find_all('div', {
                            'class': re.compile('^footnotes$|^dropdowns$|^crossrefs$|^passage-other-trans$')}) \
            + soup.find_all('span', {'class': 'selah'}) \
            + soup.find_all('selah') \
            + soup.find_all('p', {'class': 'translation-note'})
        [tag.decompose() for tag in removable_tags]

        # <br> tags will naturally be ignored when getting text
        [br.replace_with('\n') for br in soup.find_all('br')]
        # Convert chapter numbers into new lines
        [chapter_num.replace_with('\n') for chapter_num in soup.find_all('span', {'class': 'chapternum'})]
        # Preserve superscript verse numbers by using their Unicode counterparts
        # Add in the custom passage separator as well while access to the verse numbers is still available
        [sup.replace_with('{0}{1}'.format(self.passage_separator, common.superscript_numbers(sup.text)))
         for sup in soup.find_all('sup', {'class': 'versenum'})]
        # Some verses such as Nehemiah 7:30 - 42 store text in a <table> instead of <p>, which means
        # spacing is not preserved when collecting the text. Therefore, a space is manually injected
        # onto the end of the left cell's text to stop it from joining the right cell's text.
        # Note: Python "double colon" syntax for lists is used to retrieve items at every N interval including 0.
        # TODO: If a verse with >2 columns is found, this WILL need to be updated to be more dynamic
        [td.replace_with('{0} '.format(td.text)) for td in soup.find_all('td')[::2]]
        # Preserve paragraph spacing by manually pre-pending a new line
        # THIS MUST BE THE LAST PROCESSING STEP because doing this earlier interferes with other replacements
        [p.replace_with('\n{0}'.format(p.text)) for p in soup.find_all('p')]

        # Convert non-breaking spaces to normal spaces when retrieving the raw passage contents
        raw_passage_text = soup.find('div', {'class': 'passage-content'}).text.replace('\xa0', ' ')
        # To account for spaces between tags that end up blending into the passage contents, this regex replacement is
        # specifically used to remove that additional spacing, since it is part of the actual page layout.
        all_text = re.sub('([^ ])  ([^ ])', r'\1 \2', raw_passage_text)

        # Remove all superscript numbers if the passage numbers should be hidden
        if not self.show_passage_numbers:
            all_text = common.remove_superscript_numbers_in_passage(all_text)
        # EXB has in-line notes which are usually enclosed within brackets, and should not be displayed.
        # If the in-line note is simply decomposed, removing the associated space is much more difficult.
        # Thus, the in-line note text is removed at the end, when the function is strictly handling the passage text
        # to eliminate both the in-line note and its space in an easy manner.
        if translation == 'EXB':
            all_text = re.sub('\s\[.+?\]', '', all_text)
        elif translation == 'NASB':
            # NASB includes asterisks on certain verbs in the New Testament. This is an in-line marker that the verb
            # has been translated from present-tense Greek to past-tense English for better flow in modern usage.
            # As it is not actually part of the passage text itself, this is expected to be ignored.
            # Also note that this is a naive replacement - fortunately, asterisks do not seem to be used as a proper
            # text character anywhere in the NASB Bible.
            all_text = all_text.replace('*', '')

        if not self.output_as_list:
            # Restore the original passage separator to hide the special list-splitting pattern from end users
            self.passage_separator = temp_passage_separator
            # Do any final touch-ups to the passage contents before outputting the string
            return all_text.strip()

        # At this point, the expectation is that the return value is a list of passages
        passage_list = re.split(self.passage_separator, all_text.strip())
        # Remove the first empty item, even if just composed of whitespace characters
        if len(passage_list[0]) <= 0 or passage_list[0].isspace():
            passage_list.pop(0)
        # Restore the original passage separator to hide the special list-splitting pattern from end users
        self.passage_separator = temp_passage_separator
        # Since this is the end of the method, the logic may as well return the list comprehension result
        # rather than spend the extra effort to modify the existing passage list and then return the result.
        if self.strip_excess_whitespace_from_list:
            return [passage.strip() for passage in passage_list]
        return passage_list

if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
