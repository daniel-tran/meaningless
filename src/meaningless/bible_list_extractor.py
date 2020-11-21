import re
from meaningless import bible_extractor
from meaningless.utilities import common


def get_passage(book, chapter, passage, show_passage_numbers=True, translation='NIV', strip_whitespaces=False):
    """
    Gets a single passage from the web extractor.
    :param book: Name of the book
    :param chapter: Chapter number
    :param passage: Passage number
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_whitespaces: If True, passages do not retain leading and trailing whitespaces and newline characters.
    :return: List containing the passage text as a single element.
    """
    return get_passage_as_list('{0} {1}:{2}'.format(book, chapter, passage), show_passage_numbers, translation,
                               strip_whitespaces)


def get_passages(book, chapter, passage_from, passage_to, show_passage_numbers=True, translation='NIV',
                 strip_whitespaces=False):
    """
    Gets a range of passages of the same chapter from the web extractor.
    :param book: Name of the book
    :param chapter: Chapter number
    :param passage_from: First passage number to get
    :param passage_to: Last passage number to get
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_whitespaces: If True, passages do not retain leading and trailing whitespaces and newline characters.
    :return: List of passages between passage_from and passage_to (inclusive) from the given chapter.
    """
    return get_passage_as_list('{0} {1}:{2} - {3}'.format(book, chapter, passage_from, passage_to),
                               show_passage_numbers, translation, strip_whitespaces)


def get_chapter(book, chapter, show_passage_numbers=True, translation='NIV', strip_whitespaces=False):
    """
    Gets a single chapter from the web extractor.
    :param book: Name of the book
    :param chapter: Chapter number
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_whitespaces: If True, passages do not retain leading and trailing whitespaces and newline characters.
    :return: List of passages from the given chapter.
    """
    return get_passage_as_list('{0} {1}'.format(book, chapter), show_passage_numbers, translation, strip_whitespaces)


def get_chapters(book, chapter_from, chapter_to, show_passage_numbers=True, translation='NIV', strip_whitespaces=False):
    """
    Gets a range of passages from a specified chapters selection from the web extractor.
    :param book: Name of the book
    :param chapter_from: First chapter number to get
    :param chapter_to: Last chapter number to get
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_whitespaces: If True, passages do not retain leading and trailing whitespaces and newline characters.
    :return: List of passages from chapter_from to chapter_to (inclusive).
    """
    chapters = []
    # Use extend to append the passages from each chapter, and not the entire chapter as one whole item
    [chapters.extend(get_chapter(book, chapter, show_passage_numbers, translation, strip_whitespaces)) for chapter in
     range(chapter_from, chapter_to + 1)]
    return chapters


def get_passage_range(book, chapter_from, passage_from, chapter_to, passage_to, show_passage_numbers=True,
                      translation='NIV', strip_whitespaces=False):
    """
    Gets a range of passages from one specific passage to another passage from the web extractor.
    :param book: Name of the book
    :param chapter_from: First chapter number to get
    :param passage_from: First passage number to get in the first chapter
    :param chapter_to: Last chapter number to get
    :param passage_to: Last passage number to get in the last chapter
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_whitespaces: If True, passages do not retain leading and trailing whitespaces and newline characters.
    :return: List of passages from the initial passage to the final passage.
    """
    # Defer to a simpler alternative function when sourcing passages from the same chapter
    if chapter_from == chapter_to:
        return get_passages(book, chapter_from, passage_from, passage_to, show_passage_numbers, translation,
                            strip_whitespaces)
    # Sandwich the full chapters between the partial first and last chapters
    return get_passages(book, chapter_from, passage_from, common.get_end_of_chapter(), show_passage_numbers,
                        translation, strip_whitespaces) + \
        get_chapters(book, chapter_from + 1, chapter_to - 1, show_passage_numbers, translation, strip_whitespaces) + \
        get_passages(book, chapter_to, 1, passage_to, show_passage_numbers, translation, strip_whitespaces)


def get_book(book, show_passage_numbers=True, translation='NIV', strip_whitespaces=False):
    """
    Gets all chapters for a specific book from the web extractor.
    :param book: Name of the book
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_whitespaces: If True, passages do not retain leading and trailing whitespaces and newline characters.
    :return: List of passages from the specified book
    """
    return get_chapters(book, 1, common.get_chapter_count(book, translation), show_passage_numbers,
                        translation, strip_whitespaces)


def get_passage_as_list(passage_name, show_passage_numbers=True, translation='NIV', strip_whitespaces=False):
    """
    Gets all the text for a particular Bible passage from www.biblegateway.com, as a list of strings.
    :param passage_name: Name of the Bible passage which is valid when used on www.biblegateway.com
    :param show_passage_numbers: If True, passage numbers are provided at the start of each passage's text.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_whitespaces: If True, passages do not retain leading and trailing whitespaces and newline characters.
                              This can be useful in contexts that do not require passages to be appended to each other.
    :return: Bible passage as a list
    """
    # Use a string that is guaranteed to not occur anywhere in the Bible in any translation.
    # This now becomes the splitting string so that superscript passage numbers can be preserved.
    passage_separator = '-_-'
    passage_text = bible_extractor.get_passage(passage_name, passage_separator=passage_separator,
                                               show_passage_numbers=show_passage_numbers, translation=translation)

    passage_list = re.split(passage_separator, passage_text)
    # Remove the first empty item
    if len(passage_list[0]) <= 0:
        passage_list.pop(0)
    # Since this is the end of the method, the logic may as well return the list comprehension result
    # rather than spend the extra effort to modify the existing passage list and then return the result.
    if strip_whitespaces:
        return [passage.strip() for passage in passage_list]
    return passage_list
