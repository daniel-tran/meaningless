import os
from ruamel.yaml import YAML
from ruamel.yaml.parser import ParserError
from meaningless import yaml_file_interface
import re


def __get_module_directory():
    """
    A helper function to retrieve the directory of the module & ensure YAML files can be read without path modifications
    :return: The directory to the folder that contains this Python source file
    """
    return os.path.dirname(__file__)


def __get_capped_integer(number, min_value=1, max_value=100):
    """
    A helper function to limit an integer between an upper and lower bound
    :param number: Number to keep limited
    :param min_value: Lowest possible value assigned when number is lower than this
    :param max_value: Highest possible value assigned when number is larger than this
    :return: Integer that adheres to min_value <= number <= max_value

    >>> __get_capped_integer(42)
    42
    >>> __get_capped_integer(0, min_value=7)
    7
    >>> __get_capped_integer(42, max_value=7)
    7
    """
    return min(max(number, min_value), max_value)


def get_yaml_passage(book, chapter, passage, show_passage_numbers=True):
    """
    Gets a single passage from the YAML Bible files
    :param book: Name of the book
    :param chapter: Chapter number
    :param passage: Passage number
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :return: The passage as text. Empty string if the passage is invalid.
    """
    return get_yaml_passage_range(book, chapter, passage, chapter, passage, show_passage_numbers)


def get_yaml_passages(book, chapter, passage_from, passage_to, show_passage_numbers=True):
    """
    Gets a range of passages of the same chapter from the YAML Bible files
    :param book: Name of the book
    :param chapter: Chapter number
    :param passage_from: First passage number to get
    :param passage_to: Last passage number to get
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :return: The passages between the specified passages (inclusive) as text. Empty string if the passage is invalid.
    """
    return get_yaml_passage_range(book, chapter, passage_from, chapter, passage_to, show_passage_numbers)


def get_yaml_chapter(book, chapter, show_passage_numbers=True):
    """
    Gets a single chapter from the YAML Bible files
    :param book: Name of the book
    :param chapter: Chapter number
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :return: All passages in the chapter as text. Empty string if the passage is invalid.
    """
    translation = 'NIV'
    document = yaml_file_interface.read('{0}/{1}/{2}.yaml'.format(__get_module_directory(), translation, book))
    # Fail-fast on invalid passages
    if not document:
        print('WARNING: "{0} {1}" is not valid'.format(book, chapter))
        return ''
    chapter_length = len(document[book][chapter].keys())
    return get_yaml_passage_range(book, chapter, 1, chapter, chapter_length, show_passage_numbers)


def get_yaml_chapters(book, chapter_from, chapter_to, show_passage_numbers=True):
    """
    Gets a range of passages from a specified chapters selection from the YAML Bible files
    :param book: Name of the book
    :param chapter_from: First chapter number to get
    :param chapter_to: Last chapter number to get
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :return: All passages between the specified chapters (inclusive) as text. Empty string if the passage is invalid.
    """
    translation = 'NIV'
    document = yaml_file_interface.read('{0}/{1}/{2}.yaml'.format(__get_module_directory(), translation, book))
    # Fail-fast on invalid passages
    if not document:
        print('WARNING: "{0} {1} - {2}" is not valid'.format(book, chapter_from, chapter_to))
        return ''
    chapter_to_length = len(document[book][chapter_to].keys())
    return get_yaml_passage_range(book, chapter_from, 1, chapter_to, chapter_to_length, show_passage_numbers)


def get_yaml_passage_range(book, chapter_from, passage_from, chapter_to, passage_to, show_passage_numbers=True):
    """
    Gets a range of passages from one specific passage to another passage from the YAML Bible files
    :param book: Name of the book
    :param chapter_from: First chapter number to get
    :param passage_from: First passage number to get in the first chapter
    :param chapter_to: Last chapter number to get
    :param passage_to: Last passage number to get in the last chapter
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :return: All passages between the two passages (inclusive) as text. Empty string if the passage is invalid.
    """
    # Standardise letter casing to ensure key access errors are not caused by case sensitivity
    book = book.title()
    translation = 'NIV'
    # Use __file__ to ensure the file is read relative to the module location
    document = yaml_file_interface.read('{0}/{1}/{2}.yaml'.format(__get_module_directory(), translation, book))
    passage_list = []
    # Fail-fast on invalid passages
    if not document:
        print('WARNING: "{0} {1}:{2} - {3}:{4}" is not valid'.format(book, chapter_from, passage_from, chapter_to,
                                                                     passage_to))
        return ''
    # Apply a boundary to the chapters to prevent invalid keys being accessed
    chapter_from = __get_capped_integer(chapter_from, max_value=len(document[book].keys()))
    chapter_to = __get_capped_integer(chapter_to, max_value=len(document[book].keys()))
    # Extend the range by 1 since chapter_to is also included in the iteration
    for chapter in range(chapter_from, chapter_to + 1):
        # Determine the range of passages to extract from the chapter
        passage_initial = 1
        passage_final = len(document[book][chapter].keys())
        if chapter == chapter_from:
            # For the first chapter, an initial set of passages can be ignored (undercuts the passage selection)
            # Apply a boundary to the passage to prevent invalid keys being accessed
            passage_initial = __get_capped_integer(passage_from, max_value=passage_final)
        if chapter == chapter_to:
            # For the last chapter, a trailing set of passages can be ignored (exceeds the passage selection)
            # Apply a boundary to the passage to prevent invalid keys being accessed
            passage_final = __get_capped_integer(passage_to, max_value=passage_final)
        # Extend the range by 1 since the last passage is also included in the iteration
        [passage_list.append(document[book][chapter][passage]) for passage in range(passage_initial, passage_final + 1)]
        # Start each chapter on a new line
        passage_list.append('\n')
    # Convert the list of passages into a string, as strings are immutable and manually re-initialising a new string
    # in the loop can be costly to performance.
    all_text = ''.join([passage for passage in passage_list])
    if not show_passage_numbers:
        # Note that this is a naive replacement, but should be OK as long as the original file source was from the
        # module's pre-supplied YAML resources. Otherwise, using an external file source risks losing superscript
        # numbers that were not intended as passage numbers.
        # TODO Consider making this regex common between files?
        all_text = re.sub('[\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079]+\s', '', all_text)
    return all_text.strip()


if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
