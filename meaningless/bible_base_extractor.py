import os
from meaningless.utilities import common
from meaningless.utilities.exceptions import UnsupportedTranslationError, InvalidPassageError, TranslationMismatchError


class BaseExtractor:
    """
    An base extractor object that retrieves Bible passages from a file
    """

    def __init__(self, file_reading_function, translation='NIV', show_passage_numbers=True, output_as_list=False,
                 strip_excess_whitespace_from_list=False, default_directory=os.getcwd(),
                 use_ascii_punctuation=False, file_extension='', read_key_as_string=False):
        """
        :param file_reading_function: Function definition used to specify how to read a given file.
                                      The function should only take 1 argument, which states the file path to read.
        :type file_reading_function: object
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
        :param default_directory: Directory containing the file to read from.
                                  Defaults to the current working directory.
        :type default_directory: str
        :param use_ascii_punctuation: When True, converts all Unicode punctuation characters into their ASCII
                                      counterparts. This also applies to passage separators. Defaults to False.
        :type use_ascii_punctuation: bool
        :param file_extension: File extension used when reading from a default file when file_path is not provided.
        :type file_extension: str
        :param read_key_as_string: If True, specifies that all keys in the extracted file will be strings.
               Defaults to False.
        :type read_key_as_string: bool
        """
        self.translation = translation
        self.show_passage_numbers = show_passage_numbers
        self.output_as_list = output_as_list
        self.strip_excess_whitespace_from_list = strip_excess_whitespace_from_list
        self.default_directory = default_directory
        self.use_ascii_punctuation = use_ascii_punctuation
        self.file_extension = file_extension
        self.file_reading_function = file_reading_function
        self.read_key_as_string = read_key_as_string

    def get_passage(self, book, chapter, passage, file_path=''):
        """
        Gets a single passage from the Bible files

        :param book: Name of the book
        :type book: str
        :param chapter: Chapter number
        :type chapter: int
        :param passage: Passage number
        :type passage: str
        :param file_path: When specified, reads the file from this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name with a default
                          extension.
        :type file_path: str
        :return: The specified passage. Empty string/list if the passage is invalid.
        :rtype: str (list if self.output_as_list is True)
        """
        return self.get_passage_range(book, chapter, passage, chapter, passage, file_path)

    def get_passages(self, book, chapter, passage_from, passage_to, file_path=''):
        """
        Gets a range of passages of the same chapter from the files

        :param book: Name of the book
        :type book: str
        :param chapter: Chapter number
        :type chapter: int
        :param passage_from: First passage number to get
        :type passage_from: int
        :param passage_to: Last passage number to get
        :type passage_to: int
        :param file_path: When specified, reads the file from this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name with a default
                          extension.
        :type file_path: str
        :return: The passages between the specified passages (inclusive). Empty string/list if the passage is invalid.
        :rtype: str (list if self.output_as_list is True)
        """
        return self.get_passage_range(book, chapter, passage_from, chapter, passage_to, file_path)

    def get_chapter(self, book, chapter, file_path=''):
        """
        Gets a single chapter from the Bible files

        :param book: Name of the book
        :type book: str
        :param chapter: Chapter number
        :type chapter: int
        :param file_path: When specified, reads the file from this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name with a default
                          extension.
        :type file_path: str
        :return: All passages in the chapter. Empty string/list if the passage is invalid.
        :rtype: str (list if self.output_as_list is True)
        """
        return self.get_passage_range(book, chapter, 1, chapter, common.get_end_of_chapter(), file_path)

    def get_chapters(self, book, chapter_from, chapter_to, file_path=''):
        """
        Gets a range of passages from a specified chapters selection from the Bible files

        :param book: Name of the book
        :type book: str
        :param chapter_from: First chapter number to get
        :type chapter_from: int
        :param chapter_to: Last chapter number to get
        :type chapter_to: int
        :param file_path: When specified, reads the file from this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name with a default
                          extension.
        :type file_path: str
        :return: All passages between the specified chapters (inclusive). Empty string/list if the passage is invalid.
        :rtype: str (list if self.output_as_list is True)
        """
        return self.get_passage_range(book, chapter_from, 1, chapter_to, common.get_end_of_chapter(), file_path)

    def get_book(self, book, file_path=''):
        """
        Gets all chapters for a specific book from the Bible files

        :param book: Name of the book
        :type book: str
        :param file_path: When specified, reads the file from this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name with a default
                          extension.
        :type file_path: str
        :return: All passages in the specified book. Empty string/list if the passage is invalid.
        :rtype: str (list if self.output_as_list is True)
        """
        return self.get_chapters(book, 1, common.get_chapter_count(book, self.translation), file_path)

    def get_passage_range(self, book, chapter_from, passage_from, chapter_to, passage_to, file_path=''):
        """
        Gets a range of passages from one specific passage to another passage from the Bible files

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
        :param file_path: When specified, reads the file from this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name with a default
                          extension.
        :type file_path: str
        :return: All passages between the specified passages (inclusive). Empty string/list if the passage is invalid.
        :rtype: str (list if self.output_as_list is True)
        """
        translation = self.translation.upper()
        if common.is_unsupported_translation(translation):
            raise UnsupportedTranslationError(translation)
        # Standardise letter casing to ensure key access errors are not caused by case sensitivity
        book_name = book.title()
        if len(file_path) > 0:
            file_to_read = file_path
        else:
            file_to_read = os.path.join(self.default_directory, '{0}{1}'.format(book_name, self.file_extension))
        document = self.file_reading_function(file_to_read)
        passage_list = []
        # Fail-fast on invalid passages
        if not document:
            raise InvalidPassageError(book_name, chapter_from, passage_from, chapter_to, passage_to, translation)
        # Ensure matching translations are used in the extractor and file to ensure the correct translation is used.
        # Otherwise, the extractor could be used to read a bunch of files and each return different results
        # on the same passage even though the translation class property is unchanged.
        file_translation = document['Info']['Translation']
        if translation != file_translation:
            raise TranslationMismatchError(self.translation, file_translation)

        # Apply a boundary to the chapters to prevent invalid keys being accessed
        # Use the last key of the book, as it's not guaranteed that the number of chapters == last key
        chapter_final = common.dict_keys_to_sorted_list(document[book_name].keys())[-1]
        capped_chapter_from = common.get_capped_integer(chapter_from, max_value=chapter_final)
        capped_chapter_to = common.get_capped_integer(chapter_to, max_value=chapter_final)
        # Extend the range by 1 since chapter_to is also included in the iteration
        for chapter in range(capped_chapter_from, capped_chapter_to + 1):
            # Determine the range of passages to extract from the chapter
            passage_initial = 1
            # Use the last key of the chapter section, as it's not guaranteed that the number of passages == last key
            # Cast to an integer, as it is used in certain numeric operations later on.
            passage_final = int(common.dict_keys_to_sorted_list(document[book_name][self.__key_cast(chapter)].keys())
                                [-1])
            if chapter == capped_chapter_from:
                # For the first chapter, an initial set of passages can be ignored (undercuts the passage selection)
                # Apply a boundary to the passage to prevent invalid keys being accessed
                passage_initial = common.get_capped_integer(passage_from, max_value=passage_final)
            if chapter == capped_chapter_to:
                # For the last chapter, a trailing set of passages can be ignored (exceeds the passage selection)
                # Apply a boundary to the passage to prevent invalid keys being accessed
                passage_final = common.get_capped_integer(passage_to, max_value=passage_final)
            # Extend the range by 1 since the last passage is also included in the iteration
            [passage_list.append(document[book_name][self.__key_cast(chapter)][self.__key_cast(passage)]) for passage in
             range(passage_initial, passage_final + 1)]
            # Start each chapter on a new line when outputting as a string.
            if not self.output_as_list:
                passage_list.append('\n')

        if self.use_ascii_punctuation:
            passage_list = [common.unicode_to_ascii_punctuation(passage) for passage in passage_list]
        if not self.show_passage_numbers:
            # Note that this is a naive replacement, but should be OK as long as the original file source was from the
            # module's pre-supplied resources. Otherwise, using an external file source risks losing superscript
            # numbers that were not intended as passage numbers.
            passage_list = [common.remove_superscript_numbers_in_passage(passage) for passage in passage_list]
        if self.output_as_list:
            if self.strip_excess_whitespace_from_list:
                return [passage.strip() for passage in passage_list]
            return passage_list
        # Convert the list of passages into a string, as strings are immutable and manually re-initialising a new string
        # in the loop can be costly to performance.
        all_text = ''.join([passage for passage in passage_list])

        return all_text.strip()

    def __key_cast(self, key):
        """
        A helper function to cast a dictionary key to a string or an integer.

        :param key: Dictionary key
        :type key: str
        :return: Type-casted dictionary key
        :rtype: int or str
        """
        if self.read_key_as_string:
            return str(key)
        return int(key)
