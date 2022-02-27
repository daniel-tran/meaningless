from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re
from meaningless.utilities import common
from meaningless.utilities.exceptions import InvalidSearchError, UnsupportedTranslationError


class WebExtractor:
    """
    An extractor object that retrieves Bible passages from the Bible Gateway site.

    This does NOT extend from the BaseExtractor class, as it would expose certain attributes and function parameters
    that don't make sense for the Web Extractor and should not be interacted with (e.g. default directory, file path,
    file extension, etc.).
    """

    def __init__(self, translation='NIV', show_passage_numbers=True, output_as_list=False,
                 strip_excess_whitespace_from_list=False, use_ascii_punctuation=False):
        """
        :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
        :type translation: str
        :param show_passage_numbers: If True, any present passage numbers are preserved. Defaults to True.
        :type show_passage_numbers: bool
        :param output_as_list: When True, returns the passage data as a list of strings. Defaults to False.
        :type output_as_list: bool
        :param strip_excess_whitespace_from_list: When True and output_as_list is also True, leading and trailing
                                                  whitespace characters are removed for each string element in the list.
                                                  Defaults to False.
        :type strip_excess_whitespace_from_list: bool
        :param use_ascii_punctuation: When True, converts all Unicode punctuation characters into their ASCII
                                      counterparts. This also applies to passage separators. Defaults to False.
        :type use_ascii_punctuation: bool
        """
        self.translation = translation
        self.show_passage_numbers = show_passage_numbers
        self.output_as_list = output_as_list
        self.strip_excess_whitespace_from_list = strip_excess_whitespace_from_list
        self.use_ascii_punctuation = use_ascii_punctuation

    def get_passage(self, book, chapter, passage):
        """
        Gets a single passage from the Bible Gateway site.

        The chapter and passage parameters will be automatically adjusted to the respective chapter and passage
        boundaries of the specified book.

        :param book: Name of the book (This must match the name used by the translation)
        :type book: str
        :param chapter: Chapter number
        :type chapter: int
        :param passage: Passage number
        :type passage: int
        :return: The specified passage. Empty string/list if the passage is invalid.
        :rtype: str or list
        """
        return self.get_passage_range(book, chapter, passage, chapter, passage)

    def get_passages(self, book, chapter, passage_from, passage_to):
        """
        Gets a range of passages of the same chapter from the Bible Gateway site.

        Chapter and passage parameters will be automatically adjusted to the respective chapter and passage boundaries
        of the specified book.

        :param book: Name of the book (This must match the name used by the translation)
        :type book: str
        :param chapter: Chapter number
        :type chapter: int
        :param passage_from: First passage number to get
        :type passage_from: int
        :param passage_to: Last passage number to get
        :type passage_to: int
        :return: The passages between the specified passages (inclusive). Empty string/list if the passage is invalid.
        :rtype: str or list
        """
        return self.get_passage_range(book, chapter, passage_from, chapter, passage_to)

    def get_chapter(self, book, chapter):
        """
        Gets a single chapter from the Bible Gateway site.

        The chapter parameter will be automatically adjusted to the chapter boundaries of the specified book.

        :param book: Name of the book (This must match the name used by the translation)
        :type book: str
        :param chapter: Chapter number
        :type chapter: int
        :return: All passages in the chapter. Empty string/list if the passage is invalid.
        :rtype: str or list
        """
        return self.get_passage_range(book, chapter, 1, chapter, common.get_end_of_chapter())

    def get_chapters(self, book, chapter_from, chapter_to):
        """
        Gets a range of passages from a specified chapters selection from the Bible Gateway site.

        The chapter parameters will be automatically adjusted to the chapter boundaries of the specified book.

        :param book: Name of the book (This must match the name used by the translation)
        :type book: str
        :param chapter_from: First chapter number to get
        :type chapter_from: int
        :param chapter_to: Last chapter number to get
        :type chapter_to: int
        :return: All passages between the specified chapters (inclusive). Empty string/list if the passage is invalid.
        :rtype: str or list
        """
        return self.get_passage_range(book, chapter_from, 1, chapter_to, common.get_end_of_chapter())

    def get_book(self, book):
        """
        Gets all chapters for a specific book from the Bible Gateway site.

        :param book: Name of the book (This must match the name used by the translation)
        :type book: str
        :return: All passages in the specified book. Empty string/list if the passage is invalid.
        :rtype: str or list
        """
        return self.get_passage_range(book, 1, 1, common.get_chapter_count(book, self.translation),
                                      common.get_end_of_chapter())

    def get_passage_range(self, book, chapter_from, passage_from, chapter_to, passage_to):
        """
        Gets a range of passages from one specific passage to another passage from the Bible Gateway site.

        Chapter and passage parameters will be automatically adjusted to the respective chapter and passage boundaries
        of the specified book.

        :param book: Name of the book (This must match the name used by the translation)
        :type book: str
        :param chapter_from: First chapter number to get
        :type chapter_from: int
        :param passage_from: First passage number to get in the first chapter
        :type passage_from: int
        :param chapter_to: Last chapter number to get
        :type chapter_to: int
        :param passage_to: Last passage number to get in the last chapter
        :type passage_to: int
        :return: All passages between the specified passages (inclusive). Empty string/list if the passage is invalid.
        :rtype: str or list
        """
        # Capping the chapter and passage information, as this gets included in site search string and can cause
        # the web request to stagger if this manages to be long enough.
        capped_chapter_from = common.get_capped_integer(chapter_from,
                                                        max_value=common.get_chapter_count(book, self.translation))
        capped_passage_from = common.get_capped_integer(passage_from)
        capped_chapter_to = common.get_capped_integer(chapter_to,
                                                      max_value=common.get_chapter_count(book, self.translation))
        capped_passage_to = common.get_capped_integer(passage_to)
        # Defer to a direct search invocation when sourcing passages from the same chapter
        if capped_chapter_from == capped_chapter_to:
            return self.search('{0} {1}:{2} - {3}'.format(book, capped_chapter_from, capped_passage_from,
                                                          capped_passage_to))

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

    def search_multiple(self, passage_names):
        """
        Retrieves a set of passages directly from the Bible Gateway site. Passages can be from different books.
        The language used for the search text is independent of the translation.
        Note that the output is subject to the Bible Gateway implicit passage limit when sending the web request.

        :param passage_names: List of Bible passages that are valid when used on www.biblegateway.com
        :type passage_names: list
        :return: Bible passages with newline separators for each set of passages
        :rtype: str or list
        """
        return self.search(';'.join(passage_names))

    def search(self, passage_name):
        """
        Retrieves a specific passage directly from the Bible Gateway site.
        The language used for the search text is independent of the translation.
        Note that the output is subject to the Bible Gateway implicit passage limit when sending the web request.

        :param passage_name: Name of the Bible passage which is valid when used on www.biblegateway.com
        :type passage_name: str
        :return: Bible passage with preserved line breaks
        :rtype: str or list
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
            raise InvalidSearchError(source_site)

        # To get a list, the passage separator is given an actual practical use as an indicator of where to split
        # the string to create list elements.
        if self.output_as_list:
            passage_separator = '-_-'
        else:
            passage_separator = ''

        # Compile the list of tags to remove from the parsed web page, corresponding to the following elements:
        # h1
        #    - Ignore passage display
        # h2
        #    - Ignore chapter headings
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
        # p with 'translation-note' class
        #    - Ignore explicit translation notes in translations such as ESV
        # crossref
        #    - Ignore in-line references in translations such as WEB
        removable_tags = soup.find_all(re.compile('^h1$|^h2$|^h3$|^h4$')) \
            + soup.find_all('a', {'class': re.compile('^full-chap-link$|^bibleref$')}) \
            + soup.find_all('sup', {'class': re.compile('^crossreference$|^footnote$')}) \
            + soup.find_all('div', {
                            'class': re.compile('^footnotes$|^dropdowns$|^crossrefs$|^passage-other-trans$')}) \
            + soup.find_all('p', {'class': re.compile('^translation-note$')}) \
            + soup.find_all('crossref')
        # Normally, paragraphs with the 'first-line-none' class would contain valid passage contents.
        # In the GNV translation, this class name is specifically used for the blurb of notable chapter details.
        if translation == 'GNV':
            removable_tags += soup.find_all('p', {'class': re.compile('^first-line-none$')})
        [tag.decompose() for tag in removable_tags]

        # Compile a list of ways Psalm interludes can be found. These are to be preserved, as it would be the
        # translation team's decision to omit these from the passage, as opposed to a code-level design decision.
        # span with 'selah' class
        #    - Explicit Psalm interludes in the translations such as NLT and CEB
        # i with 'selah' class
        #    - Explicit Psalm interludes in the translations such as NKJV
        # selah
        #    - Explicit Psalm interludes in the translations such as HCSB
        interludes = soup.find_all('span', {'class': 'selah'}) \
            + soup.find_all('i', {'class': 'selah'}) \
            + soup.find_all('selah')
        # Psalm interludes may or may not have a leading space, depending on the translation.
        # In any case, always add one in so that the interlude doesn't meld into the passage contents.
        # To account for double spaces, this relies on a regex replacement later on to convert down to a single space.
        [interlude.replace_with(' {0}'.format(interlude.text)) for interlude in interludes]
        # <br> tags will naturally be ignored when getting text
        [br.replace_with('\n') for br in soup.find_all('br')]
        # The versenum tag appears in only a few translations such as NIVUK, and is difficult to handle because
        # its child tags are usually decomposed before this point, but space padding seems to take its place.
        # Interestingly, the tag itself can be replaced with a placeholder which itself can be removed eventually,
        # though it needs to be 2 or more characters long to reduce the total number of spaces in the final result
        # and, optionally, end with a space (this just makes it easier to get the extra spaces normalised)
        versenum_substitution_text = '--VERSE-NUM-- '
        [versenum.replace_with(versenum_substitution_text) for versenum in soup.find_all('versenum')]
        # Convert chapter numbers into new lines
        [chapter_num.replace_with('\n') for chapter_num in soup.find_all('span', {'class': 'chapternum'})]
        # Preserve superscript verse numbers by using their Unicode counterparts
        # Add in the custom passage separator as well while access to the verse numbers is still available
        [sup.replace_with('{0}{1}'.format(passage_separator, common.superscript_numbers(sup.text)))
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

        # Combine the text contents of all passage sections on the page.
        # Convert non-breaking spaces to normal spaces when retrieving the raw passage contents.
        # Also strip excess whitespaces to prevent a whitespace build-up when combining multiple passages.
        #
        # Double square brackets are removed here, as they are mostly just indicators that the passages is only kept
        # due to convention with earlier translations. This replacement is done here, as it can sometimes have a
        # trailing space which can cause double spacing, which needs to be normalised.
        raw_passage_text = '\n'.join([tag.text.replace('\xa0', ' ').strip() for tag in
                                      soup.find_all('div', {'class': 'passage-content'})]) \
            .replace('[[', '').replace(']]', '')
        # To account for spaces between tags that end up blending into the passage contents, this regex replacement is
        # specifically used to remove that additional spacing, since it is part of the actual page layout.
        all_text = re.sub('([^ ]) {2,3}([^ ])', r'\1 \2', raw_passage_text)

        # Remove all substituted versenum tags, and should also normalise the extra space
        all_text = all_text.replace(versenum_substitution_text, '')

        # Remove all superscript numbers if the passage numbers should be hidden
        if not self.show_passage_numbers:
            all_text = common.remove_superscript_numbers_in_passage(all_text)
        # Since the passage separator is prepended on all passages, the first occurrence is to be removed
        # as the separator is only needed between passages.

        # Perform ASCII punctuation conversion after hiding superscript numbers to process a slightly shorter string
        if self.use_ascii_punctuation:
            all_text = common.unicode_to_ascii_punctuation(all_text)

        # Some translations include asterisks on certain words in the New Testament. This usually indicates an in-line
        # marker that the word has been translated from present-tense Greek to past-tense English for better flow
        # in modern usage, though not all translations provide consistent footnotes on what the asterisk implies.
        # As it is not actually part of the passage text itself, this is expected to be ignored.
        # Also note that this is a naive replacement - fortunately, asterisks do not seem to be used as a proper
        # text character anywhere in the currently supported Bible translations.
        all_text = all_text.replace('*', '')
        # Translations such as GW add these text markers around certain words, which can be removed
        #
        # Translations such as JUB append a pilcrow character at the start of certain passages, which can be removed.
        # These usually have a trailing space, which also needs to be removed to prevent double spacing.
        # This logic would need to be revisited if there are cases of pilcrows without a trailing space.
        all_text = all_text.replace('⌞', '').replace('⌟', '').replace('¶ ', '')

        if not self.output_as_list:
            # Do any final touch-ups to the passage contents before outputting the string
            return all_text.strip()

        # At this point, the expectation is that the return value is a list of passages.
        # Since the passage separator is placed before the passage number, it can cause an empty first item upon
        # splitting if the first passage has a passage number.
        # Remove the first passage separator in such scenarios to prevent this from happening.
        # Also perform a one-off strip to ensure the first passage separator is correctly identified.
        if all_text.strip().startswith(passage_separator):
            all_text = all_text.replace(passage_separator, '', 1)
        passage_list = re.split(passage_separator, all_text.strip())
        # Since this is the end of the method, the logic may as well return the list comprehension result
        # rather than spend the extra effort to modify the existing passage list and then return the result.
        if self.strip_excess_whitespace_from_list:
            return [passage.strip() for passage in passage_list]
        return passage_list
