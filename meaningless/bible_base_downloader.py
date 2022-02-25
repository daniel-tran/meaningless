import os
import multiprocessing
from meaningless.bible_web_extractor import WebExtractor
from meaningless.utilities import common
from meaningless.utilities.exceptions import UnsupportedTranslationError, InvalidPassageError


class BaseDownloader:
    """
    An downloader object that stores Bible passages into a local file
    """

    __translations_with_omitted_passages = {
        'ASV': ['Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14',
                'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 11:26', 'Mark 15:28',
                'Luke 17:36', 'Luke 23:17',
                'John 5:4',
                'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29',
                'Romans 16:24'],
        'EHV': ['Matthew 23:14',
                'Mark 15:28',
                'Luke 17:36',
                'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29',
                'Romans 16:24'],
        'ESV': ['Matthew 12:47', 'Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14',
                'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 11:26', 'Mark 15:28',
                'Luke 17:36', 'Luke 23:17',
                'John 5:4',
                'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29',
                'Romans 16:24'],
        'ESVUK': ['Matthew 12:47', 'Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14',
                  'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 11:26', 'Mark 15:28',
                  'Luke 17:36', 'Luke 23:17',
                  'John 5:4',
                  'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29',
                  'Romans 16:24'],
        'GW': ['Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14',
               'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 11:26', 'Mark 15:28',
               'Luke 17:36', 'Luke 23:17',
               'John 5:4',
               'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29',
               'Romans 16:24'],
        'ISV': ['Mark 15:28',
                'Luke 17:36',
                'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29'],
        'LEB': ['Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14',
                'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 11:26', 'Mark 15:28',
                'Luke 17:36', 'Luke 23:17',
                'John 5:4',
                'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29'],
        'NRSV': ['Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14',
                 'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 11:26', 'Mark 15:28',
                 'Luke 17:36', 'Luke 23:17',
                 'John 5:4',
                 'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29',
                 'Romans 16:24'],
        'NLT': ['Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14',
                'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 11:26', 'Mark 15:28',
                'Luke 17:36', 'Luke 23:17',
                'John 5:4',
                'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29',
                'Romans 16:24'],
        'NASB': ['Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14',
                 'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 15:28',
                 'John 5:4',
                 'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29',
                 'Romans 16:24'],
        'NET': ['Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14',
                'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 11:26', 'Mark 15:28',
                'Luke 17:36', 'Luke 23:17',
                'John 5:4',
                'Acts 8:37', 'Acts 15:34', 'Acts 28:29',
                'Romans 16:24'],
        'NOG': ['Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14',
                'Mark 9:44', 'Mark 9:46', 'Mark 11:26', 'Mark 15:28',
                'Luke 17:36', 'Luke 23:17',
                'John 5:4',
                'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29',
                'Romans 16:24'],
    }

    def __init__(self, file_writing_function, translation='NIV', show_passage_numbers=True,
                 default_directory=os.getcwd(), strip_excess_whitespace=False, enable_multiprocessing=True,
                 use_ascii_punctuation=False, file_extension='', write_key_as_string=False):
        """
        :param file_writing_function: Function definition used to specify how to write to a given file.
                                      The function should only take 2 arguments, which are the file path to write to
                                      and the in-memory object being sourced (in that order).
        :type file_writing_function: callable[[str, dict], int]
        :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
        :type translation: str
        :param show_passage_numbers: If True, any present passage numbers are preserved. Defaults to True.
        :type show_passage_numbers: bool
        :param default_directory: Directory containing the downloaded file.
                                  Defaults to the current working directory.
        :type default_directory: str
        :param strip_excess_whitespace: If True, passages don't retain leading & trailing whitespaces as well as
                                        newline characters. Defaults to False.
        :type strip_excess_whitespace: bool
        :param enable_multiprocessing: If True, downloads are performed using multiple daemon processes, resulting in
                                       lower download times by splitting computations among multiple CPU cores.
                                       Defaults to True.
        :type enable_multiprocessing: bool
        :param use_ascii_punctuation: When True, converts all Unicode punctuation characters into their ASCII
                                      counterparts. Defaults to False.
        :type use_ascii_punctuation: bool
        :param file_extension: File extension used when reading from a default file when file_path is not provided
        :type file_extension: str
        :param write_key_as_string: If True, specifies that all keys in the downloaded file are converted to strings.
               Defaults to False.
        :type write_key_as_string: bool
        """
        self.translation = translation
        self.show_passage_numbers = show_passage_numbers
        self.default_directory = default_directory
        self.strip_excess_whitespace = strip_excess_whitespace
        self.enable_multiprocessing = enable_multiprocessing
        self.use_ascii_punctuation = use_ascii_punctuation
        self.file_extension = file_extension
        self.file_writing_function = file_writing_function
        self.write_key_as_string = write_key_as_string

    def download_passage(self, book, chapter, passage, file_path=''):
        """
        Downloads a single passage as a file.

        The chapter and passage parameters will be automatically adjusted to the respective chapter and passage
        boundaries of the specified book.

        :param book: Name of the book
        :type book: str
        :param chapter: Chapter number
        :type chapter: int
        :param passage: Passage number
        :type passage: int
        :param file_path: When specified, saves the file to this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name with a default
                          extension.
        :type file_path: str
        :return: 1 if the download was successful. 0 if an error occurred.
        :rtype: int
        """
        return self.download_passage_range(book, chapter, passage, chapter, passage, file_path)

    def download_passages(self, book, chapter, passage_from, passage_to, file_path=''):
        """
        Downloads a range of passages of the same chapter as a file.

        Chapter and passage parameters will be automatically adjusted to the respective chapter and passage boundaries
        of the specified book.

        :param book: Name of the book
        :type book: str
        :param chapter: Chapter number
        :type chapter: int
        :param passage_from: First passage number to get
        :type passage_from: int
        :param passage_to: Last passage number to get
        :type passage_to: int
        :param file_path: When specified, saves the file to this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name with a default
                          extension.
        :type file_path: str
        :return: 1 if the download was successful. 0 if an error occurred.
        :rtype: int
        """
        return self.download_passage_range(book, chapter, passage_from, chapter, passage_to, file_path)

    def download_chapter(self, book, chapter, file_path=''):
        """
        Downloads a single chapter as a file.

        The chapter parameter will be automatically adjusted to the chapter boundaries of the specified book.

        :param book: Name of the book
        :type book: str
        :param chapter: Chapter number
        :type chapter: int
        :param file_path: When specified, saves the file to this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name with a default
                          extension.
        :type file_path: str
        :return: 1 if the download was successful. 0 if an error occurred.
        :rtype: int
        """
        return self.download_passage_range(book, chapter, 1, chapter, common.get_end_of_chapter(), file_path)

    def download_chapters(self, book, chapter_from, chapter_to, file_path=''):
        """
        Downloads a range of passages from a specified chapter selection as a file.

        Chapter parameters will be automatically adjusted to the chapter boundaries of the specified book.

        :param book: Name of the book
        :type book: str
        :param chapter_from: First chapter number to get
        :type chapter_from: int
        :param chapter_to: Last chapter number to get
        :type chapter_to: int
        :param file_path: When specified, saves the file to this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name with a default
                          extension.
        :type file_path: str
        :return: 1 if the download was successful. 0 if an error occurred.
        :rtype: int
        """
        return self.download_passage_range(book, chapter_from, 1, chapter_to, common.get_end_of_chapter(), file_path)

    def download_book(self, book, file_path=''):
        """
        Downloads a specific book of the Bible and saves it as a file

        :param book: Name of the book
        :type book: str
        :param file_path: When specified, saves the file to this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name with a default
                          extension.
        :type file_path: str
        :return: 1 if the download was successful. 0 if an error occurred.
        :rtype: int
        """
        return self.download_passage_range(book, 1, 1, common.get_chapter_count(book, self.translation),
                                           common.get_end_of_chapter(), file_path)

    def download_passage_range(self, book, chapter_from, passage_from, chapter_to, passage_to, file_path=''):
        """
        Downloads a range of passages from one specific passage to another passage as a file.

        Chapter and passage parameters will be automatically adjusted to the respective chapter and passage boundaries
        of the specified book.

        :param book: Name of the book
        :type book: str
        :param chapter_from: First chapter number to get
        :type chapter_from: int
        :param passage_from: First passage number to get in the first chapter
        :type passage_from: int
        :param chapter_to: Last chapter number to get
        :type chapter_to: int
        :param passage_to: Last passage number to get in the last chapter
        :type passage_to: int
        :param file_path: When specified, saves the file to this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name with a default
                          extension.
        :type file_path: str
        :return: 1 if the download was successful. 0 if an error occurred.
        :rtype: int
        """
        translation = self.translation.upper()
        if common.is_unsupported_translation(translation):
            raise UnsupportedTranslationError(translation)
        # Standardise letter casing with minimal impact to the resulting file
        book_name = book.title()

        if common.get_chapter_count(book_name, translation) <= 0:
            raise InvalidPassageError(book_name, chapter_from, passage_from, chapter_to, passage_to, translation)
        # Cap passage components to ensure input validity and minimise web requests by avoiding invalid chapters
        capped_chapter_from = common.get_capped_integer(chapter_from,
                                                        max_value=common.get_chapter_count(book_name, translation))
        capped_passage_from = common.get_capped_integer(passage_from)
        capped_chapter_to = common.get_capped_integer(chapter_to,
                                                      max_value=common.get_chapter_count(book_name, translation))
        capped_passage_to = common.get_capped_integer(passage_to)

        online_bible = WebExtractor(translation=translation, show_passage_numbers=self.show_passage_numbers,
                                    output_as_list=True, strip_excess_whitespace_from_list=self.strip_excess_whitespace,
                                    use_ascii_punctuation=self.use_ascii_punctuation)

        # Set up the base document with the root-level keys
        # Upon downloading a file, the top-level keys might be ordered differently to when they were inserted.
        # This is likely due to Python not sorting dictionary keys internally, but could be due to something else.
        # This does not affect the information contained in the downloaded file, but could affect file comparisons.
        document = {
            'Info': {
                'Language': common.get_translation_language(translation),
                'Translation': translation
            },
            book_name: {}
        }

        # Don't initialise the thread pool unless the extractor has been set to use multiprocessing.
        # This logic could be already running in a daemon process, and initialising the pool will cause an error.
        process_pool = None
        if self.enable_multiprocessing:
            process_pool = multiprocessing.Pool()
        process_results = []

        # Range is extended by 1 to include chapter_to in the loop iteration
        chapter_range = range(capped_chapter_from, capped_chapter_to + 1)
        for chapter in chapter_range:
            passage_initial = 1
            passage_final = common.get_end_of_chapter()
            # Exclude a certain first half of the initial chapter based on where the passage start should be
            if chapter == capped_chapter_from:
                passage_initial = capped_passage_from
            # Exclude a certain last half of the last chapter based on where the passage end should be
            if chapter == capped_chapter_to:
                passage_final = capped_passage_to

            if self.enable_multiprocessing:
                # Asynchronously obtain each set of passages to reduce overall download time.
                # These are daemon processes, so these shouldn't block the program from exiting and should be
                # expected to be garbage collected if the main process is stopped.
                process = process_pool.apply_async(self._get_passages_dict, (online_bible, book_name, chapter,
                                                                             passage_initial, passage_final),
                                                   error_callback=self.__handle_exception_from_process)
                # Add the process result to the list and extract the value later to prioritise doing more work
                process_results.append(process)
            else:
                document[book_name][self.__key_cast(chapter)] = self._get_passages_dict(online_bible, book_name,
                                                                                        chapter, passage_initial,
                                                                                        passage_final)

        if self.enable_multiprocessing:
            # Close the pool manually, as the garbage collector might not dispose of this automatically
            process_pool.close()
            # Explicitly wait for the processes to finish up in case some processes have heavy workloads
            process_pool.join()
            # When multiprocessing, all process results should be retrieved as a batch operation to minimise
            # the total time cost associated with the "get" method for each result.
            document[book_name] = {self.__key_cast(chapter): process_results.pop(0).get() for chapter in chapter_range}

        if len(file_path) <= 0:
            file_location = os.path.join(self.default_directory, '{0}{1}'.format(book_name, self.file_extension))
        else:
            file_location = file_path
        return self.file_writing_function(file_location, document)

    @staticmethod
    def __handle_exception_from_process(exception):
        """
        A helper function that gets run an exception is received when downloading passages.
        This is not a top-level global function, as it is intended to be solely used within this class.

        :param exception: Exception object that is re-raised after this method completes.
        :type exception: object
        """
        # Clear the arguments to prevent "stacking" of exception error messages.
        # An empty tuple means the user has to search elsewhere in the stack trace to find the point of failure.
        exception.args = ()

    def _get_passages_dict(self, online_bible, book, chapter, passage_from, passage_to):
        """
        A helper function that obtains a range of passages and organises them as a dictionary for output.
        Not to be exposed as a usable method, as this function mostly exists so that passage retrieval can be done
        in a multi-processed way. Pre-pending the method name with double underscores causes referencing issues.

        :param online_bible: Instance of WebExtractor to use to download the passages
        :type online_bible: WebExtractor
        :param book: Name of the book
        :type book: str
        :param chapter: Chapter number
        :type chapter: int
        :param passage_from: First passage number to get
        :type passage_from: int
        :param passage_to: Last passage number to get
        :type passage_to: int
        :return: Dictionary of passages, keyed on passage number
        :rtype: dict
        """
        online_bible.output_as_list = True
        passage_list = online_bible.get_passages(book, chapter, passage_from, passage_to)
        # passage_num is the numerical representation of the Unicode passage number at the start of each passage
        passage_num = passage_from
        # self.translation is not used, since getting this far means that the translation used in the
        # earlier call to get_passages is guaranteed to be valid.
        is_translation_with_omitted_passages = online_bible.translation in \
            self.__translations_with_omitted_passages.keys()
        passages = {}
        for passage in passage_list:
            if is_translation_with_omitted_passages:
                # This logic handles translations that omit passages, and have are not considered as valid verse on
                # the Bible Gateway site. It works by checking the passage against the list of known omitted
                # passages for this particular translation, and assigning an empty string if it is omitted.
                # This is to ensure the passage key matches the actual passage contents,
                # regardless of translation.
                passage_string = '{0} {1}:{2}'.format(book, chapter, passage_num)
                if passage_string in self.__translations_with_omitted_passages[online_bible.translation]:
                    passages[self.__key_cast(passage_num)] = ''
                    # Since this passage isn't supposed to exist in the given translation but it is still registered
                    # in the file, the number is upped twice in this loop iteration - once for the omitted
                    # passage and once for the passage after the omitted passage (whose contents is accessible in
                    # this particular iteration)
                    passage_num += 1

            # First passage of the chapter may not always have a verse number.
            # Unclear if this is a formatting issue on the Bible Gateway site, but it is added for consistency.
            # This is not done on the web extractor due to the difficulty of selecting the first passage in an
            # arbitrary range.
            if passage_num == 1 and self.show_passage_numbers and not passage.startswith('¹ '):
                passage = '¹ {0}'.format(passage)

            passages[self.__key_cast(passage_num)] = passage
            passage_num += 1
        return passages

    def __key_cast(self, key):
        """
        A helper function to cast a dictionary key to a string or an integer.

        :param key: Dictionary key
        :type key: int or str
        :return: Type-casted dictionary key
        :rtype: int or str
        """
        return common.cast_to_str_or_int(key, self.write_key_as_string)
