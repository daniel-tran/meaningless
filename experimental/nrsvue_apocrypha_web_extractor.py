import sys
from timeit import default_timer
sys.path.append('../')
from meaningless import WebExtractor
from meaningless.utilities import common, exceptions


class NonApocryphaSearchError(exceptions.BaseError):
    """
    An exception thrown when searching for a book that is not part of the NRSVUE Apocrypha
    """

    def __init__(self, book):
        """
        :param book: The book name
        :type book: str
        """
        super(NonApocryphaSearchError, self).__init__(f'{book} is not part of the NRSVUE Apocrypha')
        self.book = book


class ApocryphaWebExtractor(WebExtractor):
    """
    An experimental extractor object that specifically retrieves Bible passages from the Apocrypha books
    of the NRSVUE translation from Bible Gateway site.
    """

    __apocrypha_chapter_count_mappings = {
        'Tobit': 14,
        'Judith': 16,
        'Greek Esther': 10,
        'Wisdom Of Solomon': 19,
        'Sirach': 51,
        'Baruch': 5,
        'Letter Of Jeremiah': 1,
        'Prayer Of Azariah': 1,
        'Susanna': 1,
        'Bel And The Dragon': 1,
        '1 Maccabees': 16,
        '2 Maccabees': 15,
        '1 Esdras': 9,
        'Prayer Of Manasseh': 1,
        'Psalm 151': 1,
        '3 Maccabees': 7,
        '2 Esdras': 16,
        '4 Maccabees': 18
    }

    def __init__(self, translation='NRSVUE', show_passage_numbers=True, output_as_list=False,
                 strip_excess_whitespace_from_list=False, use_ascii_punctuation=False):
        """
        :param translation: Translation code for the particular passage. Providing this parameter deliberately has no
                            effect and is only supported so that this class can be swapped out with the WebExtractor in
                            the BaseDownloader class and enable writing Apocrypha passages to a local file
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
        super().__init__('NRSVUE', show_passage_numbers, output_as_list, strip_excess_whitespace_from_list,
                         use_ascii_punctuation)

    def __process_special_passage(self, passage):
        """
        Applies the relevant transformations to the passage contents, under the assumption that it is pre-processed

        :param passage: Raw passage contents
        :type passage: str
        :return: The transformed passage contents
        :rtype: str or list
        """
        modified_passage = passage
        if not self.show_passage_numbers:
            modified_passage = common.remove_superscript_numbers_in_passage(modified_passage)
        if self.use_ascii_punctuation:
            modified_passage = common.unicode_to_ascii_punctuation(modified_passage)
        if not self.output_as_list:
            return modified_passage
        if self.strip_excess_whitespace_from_list:
            modified_passage = modified_passage.strip()
        return [modified_passage]

    def get_passage(self, book, chapter, passage):
        """
        Gets a single passage from the Bible Gateway site.

        For simplicity, the chapter and passage parameters will NOT be adjusted to the respective chapter and passage
        boundaries of the specified book.

        :param book: Name of the book (This must match the name used by the translation)
        :type book: str
        :param chapter: Chapter number
        :type chapter: int
        :param passage: Passage number
        :type passage: int
        :return: The specified passage. Empty string/list if the passage is invalid. May also throw an exception.
        :rtype: str or list
        """
        # The general idea is that there are some passages which are very difficult to process in a generic way.
        # For those passages, return the raw contents which is provided through manual specification.
        # For everything else, the usual WebExtractor.search() function should be good enough.

        preprocessed_passages = {
            'Tobit 1:1': 'The book of the words of Tobit son of Tobiel son of Hananiel son of Aduel son of Gabael son '
                         'of Raphael son of Raguel of the descendants of Asiel, of the tribe of Naphtali,',
            'Greek Esther 1:1': 'It was after this that the following things happened in the days of '
                                'Artaxerxes, the same Artaxerxes who ruled over one hundred '
                                'twenty-seven provinces from India to Ethiopia.',
            'Greek Esther 3:13': '¹³ Instructions were sent by couriers throughout all the empire of '
                                 'Artaxerxes to destroy the Jewish people in a single day of the '
                                 'twelfth month, which is Adar, and to plunder their goods.',
            'Greek Esther 8:12': '¹² on a single day, the thirteenth of the twelfth month, '
                                 'which is Adar, throughout all the kingdom of Artaxerxes.',
            'Greek Esther 10:13': '¹³ So they will observe these days in the month of Adar, on the '
                                  'fourteenth and fifteenth of that month, with an assembly and joy '
                                  'and gladness before God, from generation to generation forever '
                                  'among his people Israel.”',
            'Sirach 1:1': 'All wisdom is from the Lord,\nand with him it remains forever.',
            'Letter Of Jeremiah 1:1': 'Because of the sins that you have committed before God, you will be taken to '
                                      'Babylon as exiles by Nebuchadnezzar, king of the Babylonians.',
            'Prayer Of Azariah 1:1': '¹ They walked around in the midst of the flames, '
                                     'singing hymns to God and blessing the Lord.',
            '1 Esdras 1:1': 'Josiah kept the Passover to his Lord in Jerusalem; he killed the '
                            'Passover lamb on the fourteenth day of the first month,',
            '2 Esdras 1:1': 'The book of the prophet Ezra son of Seraiah, son of Azariah, son of Hilkiah, '
                            'son of Shallum, son of Zadok, son of Ahitub,',
        }

        passage_key = f'{book.title()} {chapter}:{passage}'
        if passage_key in preprocessed_passages.keys():
            return self.__process_special_passage(preprocessed_passages[passage_key])

        return super().search(f'{book} {chapter}:{passage}')

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
        book_name = book.title()
        if book_name not in self.__apocrypha_chapter_count_mappings.keys():
            # Uncomment the below 'return' statement to enable primitive support for non-Apocrypha books.
            # Note that super().get_passage_range will fail, since it's already been overridden here.
            #
            # return super().search(f'{book} {chapter_from}:{passage_from} - {chapter_to}:{passage_to}')
            raise NonApocryphaSearchError(book_name)

        # Capping the chapter and passage information, as this gets included in site search string and can cause
        # the web request to stagger if this manages to be long enough.
        capped_chapter_from = common.get_capped_integer(chapter_from,
                                                        max_value=self.__apocrypha_chapter_count_mappings[book_name])
        capped_passage_from = common.get_capped_integer(passage_from, max_value=common.get_end_of_chapter())
        capped_chapter_to = common.get_capped_integer(chapter_to,
                                                      max_value=self.__apocrypha_chapter_count_mappings[book_name])
        capped_passage_to = common.get_capped_integer(passage_to, max_value=common.get_end_of_chapter())

        output = []
        chapter = capped_chapter_from
        # Obtains each individual passage and glues the total contents together at the end.
        # This needs to be done this way, because some passages are very difficult to process and this is the
        # easiest way to apply the alternative logic without too much complexity.
        # This could be done in a multi-processed way, but it doesn't guarantee ordering (which is needed in this case).
        while chapter <= capped_chapter_to:
            # For the first and last chapter, only a partial chapter is required
            passage = capped_passage_from if chapter == capped_chapter_from else 1
            passage_end = capped_passage_to if chapter == capped_chapter_to else common.get_end_of_chapter()

            while passage <= passage_end:
                try:
                    # To get to the end of a chapter, either figure out what the highest passage number is for a
                    # given chapter, or naively keep requesting passages until one is requested which doesn't exist
                    output.append(self.get_passage(book_name, chapter, passage))
                except exceptions.InvalidSearchError:
                    # TODO: This would not work with books which have non-existent passages
                    break
                passage += 1
            chapter += 1

        if self.output_as_list:
            # Flattens the data structure from a list of lists to a normal list
            return [chapter for chapter_list in output for chapter in chapter_list]
        return ''.join(output)

    def search(self, passage_name):
        """
        This method is not supported for this class because the output is not guaranteed to be correct in all cases
        """
        pass

    def search_multiple(self, passage_names):
        """
        This method is not supported for this class because the output is not guaranteed to be correct in all cases
        """
        pass


def print_time_elapsed(start_time, end_time):
    """
    Prints the time elapsed from two start points

    :param start_time: Time when measured operation began
    :type start_time: float
    :param end_time: Time when measured operation ended
    :type end_time: float
    :return: No return value
    """
    print(f'Time elapsed: {round(end_time - start_time, 3)} seconds')


if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    extractor = ApocryphaWebExtractor()

    start = default_timer()
    print(extractor.get_passage('3 Maccabees', 2, 1))
    end = default_timer()
    print_time_elapsed(start, end)

    input('Next: Pre-processed passages that are normally difficult to extract programmatically')
    start = default_timer()
    print(extractor.get_passage('Tobit', 1, 1))
    print(extractor.get_passage('Greek Esther', 1, 1))
    print(extractor.get_passage('Greek Esther', 3, 13))
    print(extractor.get_passage('Greek Esther', 8, 12))
    print(extractor.get_passage('Greek Esther', 10, 13))
    print(extractor.get_passage('Sirach', 1, 1))
    print(extractor.get_passage('Letter of Jeremiah', 1, 1))
    print(extractor.get_passage('Prayer of Azariah', 1, 1))
    print(extractor.get_passage('1 Esdras', 1, 1))
    print(extractor.get_passage('2 Esdras', 1, 1))
    end = default_timer()
    print_time_elapsed(start, end)

    input('Next: Get a range of passages')
    start = default_timer()
    print(extractor.get_passages('Greek Esther', 10, 1, 3))
    end = default_timer()
    print_time_elapsed(start, end)

    input('Next: Get a chapter')
    start = default_timer()
    print(extractor.get_chapter('Greek Esther', 10))
    end = default_timer()
    print_time_elapsed(start, end)

    input('Next: Get a range of chapters')
    start = default_timer()
    print(extractor.get_chapters('Greek Esther', 7, 8))
    end = default_timer()
    print_time_elapsed(start, end)

    input('Next: Get a range of passages that crosses the chapter boundary')
    start = default_timer()
    print(extractor.get_passage_range('Greek Esther', 6, 13, 7, 2))
    end = default_timer()
    print_time_elapsed(start, end)

    input('Next: Get an entire book')
    start = default_timer()
    print(extractor.get_book('Prayer of Manasseh'))
    end = default_timer()
    print_time_elapsed(start, end)

    input('Next: Get passages from a non-Apocrypha book (raises an exception)')
    try:
        print(extractor.get_passage_range('Acts', 6, 13, 7, 2))
    except NonApocryphaSearchError:
        print(sys.exc_info())
