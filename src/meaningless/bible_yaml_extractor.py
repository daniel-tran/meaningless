import os
from ruamel.yaml import YAML
from ruamel.yaml.parser import ParserError
from meaningless.utilities import yaml_file_interface, common
import re


class YAMLExtractor:

    def get_local_yaml_file_path(self, book):
        """
        A local helper function to retrieve the file path to a locally sourced YAML file
        :param book: Name of the book
        :return: The file path to the YAML file
        """
        return os.path.join(os.path.dirname(__file__), 'translations', self.translation, '{0}.yaml'.format(book))

    def __init__(self, translation='NIV', show_passage_numbers=True, output_as_list=False,
                 strip_excess_whitespace_from_list=False, passage_separator=''):
        """
        :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
        :param show_passage_numbers: If True, any present passage numbers are preserved.
        :param output_as_list: When True, returns the passage data as a list of strings.
        :param strip_excess_whitespace_from_list: When True and output_as_list is also True, leading and trailing
                                                  whitespace characters are removed for each string element in the list.
        :param passage_separator: When output_as_list is False, an optional string added to the front of a passage
                                  (placed before the passage number). Defaults to the empty string.
        """
        self.translation = translation
        self.show_passage_numbers = show_passage_numbers
        self.output_as_list = output_as_list
        self.strip_excess_whitespace_from_list = strip_excess_whitespace_from_list
        self.passage_separator = passage_separator

    def get_passage(self, book, chapter, passage):
        """
        Gets a single passage from the YAML Bible files
        :param book: Name of the book
        :param chapter: Chapter number
        :param passage: Passage number
        :return: The specified passage. Empty string/list if the passage is invalid.
        """
        return self.get_passage_range(book, chapter, passage, chapter, passage)

    def get_passages(self, book, chapter, passage_from, passage_to):
        """
        Gets a range of passages of the same chapter from the YAML Bible files
        :param book: Name of the book
        :param chapter: Chapter number
        :param passage_from: First passage number to get
        :param passage_to: Last passage number to get
        :return: The passages between the specified passages (inclusive). Empty string/list if the passage is invalid.
        """
        return self.get_passage_range(book, chapter, passage_from, chapter, passage_to)

    def get_chapter(self, book, chapter):
        """
        Gets a single chapter from the YAML Bible files
        :param book: Name of the book
        :param chapter: Chapter number
        :return: All passages in the chapter. Empty string/list if the passage is invalid.
        """
        document = yaml_file_interface.read(self.get_local_yaml_file_path(book))
        # Fail-fast on invalid passages
        if not document:
            print('WARNING: "{0} {1}" is not valid'.format(book, chapter))
            return common.get_empty_data(self.output_as_list)
        chapter_length = len(document[book][chapter].keys())
        return self.get_passage_range(book, chapter, 1, chapter, chapter_length)

    def get_chapters(self, book, chapter_from, chapter_to):
        """
        Gets a range of passages from a specified chapters selection from the YAML Bible files
        :param book: Name of the book
        :param chapter_from: First chapter number to get
        :param chapter_to: Last chapter number to get
        :return: All passages between the specified chapters (inclusive). Empty string/list if the passage is invalid.
        """
        document = yaml_file_interface.read(self.get_local_yaml_file_path(book))
        # Fail-fast on invalid passages
        if not document:
            print('WARNING: "{0} {1} - {2}" is not valid'.format(book, chapter_from, chapter_to))
            return common.get_empty_data(self.output_as_list)
        chapter_to_length = len(document[book][chapter_to].keys())
        return self.get_passage_range(book, chapter_from, 1, chapter_to, chapter_to_length)

    def get_book(self, book):
        """
        Gets all chapters for a specific book from the YAML Bible files
        :param book: Name of the book
        :return: All passages in the specified book. Empty string/list if the passage is invalid.
        """
        return self.get_chapters(book, 1, common.get_chapter_count(book, self.translation))

    def get_passage_range(self, book, chapter_from, passage_from, chapter_to, passage_to):
        """
        Gets a range of passages from one specific passage to another passage from the YAML Bible files
        :param book: Name of the book
        :param chapter_from: First chapter number to get
        :param passage_from: First passage number to get in the first chapter
        :param chapter_to: Last chapter number to get
        :param passage_to: Last passage number to get in the last chapter
        :return: All passages between the specified passages (inclusive). Empty string/list if the passage is invalid.
        """
        # Standardise letter casing to ensure key access errors are not caused by case sensitivity
        book = book.title()
        document = yaml_file_interface.read(self.get_local_yaml_file_path(book))
        passage_list = []
        # Fail-fast on invalid passages
        if not document:
            print('WARNING: "{0} {1}:{2} - {3}:{4}" is not valid'.format(book, chapter_from, passage_from, chapter_to,
                                                                         passage_to))
            return common.get_empty_data(self.output_as_list)
        # Apply a boundary to the chapters to prevent invalid keys being accessed
        chapter_from = common.get_capped_integer(chapter_from, max_value=len(document[book].keys()))
        chapter_to = common.get_capped_integer(chapter_to, max_value=len(document[book].keys()))
        # Extend the range by 1 since chapter_to is also included in the iteration
        for chapter in range(chapter_from, chapter_to + 1):
            # Determine the range of passages to extract from the chapter
            passage_initial = 1
            passage_final = len(document[book][chapter].keys())
            if chapter == chapter_from:
                # For the first chapter, an initial set of passages can be ignored (undercuts the passage selection)
                # Apply a boundary to the passage to prevent invalid keys being accessed
                passage_initial = common.get_capped_integer(passage_from, max_value=passage_final)
            if chapter == chapter_to:
                # For the last chapter, a trailing set of passages can be ignored (exceeds the passage selection)
                # Apply a boundary to the passage to prevent invalid keys being accessed
                passage_final = common.get_capped_integer(passage_to, max_value=passage_final)
            # Extend the range by 1 since the last passage is also included in the iteration
            [passage_list.append(document[book][chapter][passage]) for passage in
             range(passage_initial, passage_final + 1)]
            # Start each chapter on a new line when outputting as a string. Use the passage separator if it is set, to
            # ensure uniform passage separation regardless of chapter boundaries.
            if not self.output_as_list and len(self.passage_separator) <= 0:
                passage_list.append('\n')

        if not self.show_passage_numbers:
            # Note that this is a naive replacement, but should be OK as long as the original file source was from the
            # module's pre-supplied YAML resources. Otherwise, using an external file source risks losing superscript
            # numbers that were not intended as passage numbers.
            passage_list = [common.remove_superscript_numbers_in_passage(passage) for passage in passage_list]
        if self.output_as_list:
            if self.strip_excess_whitespace_from_list:
                return [passage.strip() for passage in passage_list]
            return passage_list
        # Convert the list of passages into a string, as strings are immutable and manually re-initialising a new string
        # in the loop can be costly to performance.
        all_text = self.passage_separator.join([passage for passage in passage_list])

        return all_text.strip()

if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
