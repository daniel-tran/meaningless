import re
from meaningless import bible_extractor


def get_passage(book, chapter, passage, show_passage_numbers=True, translation='NIV'):
    return get_passage_as_list('{0} {1}:{2}'.format(book, chapter, passage), show_passage_numbers, translation)


def get_passages(book, chapter, passage_from, passage_to, show_passage_numbers=True, translation='NIV'):
    return get_passage_as_list('{0} {1}:{2} - {3}'.format(book, chapter, passage_from, passage_to),
                               show_passage_numbers, translation)


def get_chapter(book, chapter, show_passage_numbers=True, translation='NIV'):
    return get_passage_as_list('{0} {1}'.format(book, chapter), show_passage_numbers, translation)


def get_chapters(book, chapter_from, chapter_to, show_passage_numbers=True, translation='NIV'):
    chapters = []
    # Use extend to append the passages from each chapter, and not the entire chapter as one whole item
    [chapters.extend(get_chapter(book, chapter, show_passage_numbers, translation)) for chapter in
     range(chapter_from, chapter_to + 1)]
    return chapters


def get_passage_range(book, chapter_from, passage_from, chapter_to, passage_to, show_passage_numbers=True,
                      translation='NIV'):
    # Defer to a simpler alternative function when sourcing passages from the same chapter
    if chapter_from == chapter_to:
        return get_passages(book, chapter_from, passage_from, passage_to, show_passage_numbers, translation)
    # Sandwich the full chapters between the partial first and last chapters
    return get_passages(book, chapter_from, passage_from, 9000, show_passage_numbers, translation) + \
        get_chapters(book, chapter_from + 1, chapter_to - 1, show_passage_numbers, translation) + \
        get_passages(book, chapter_to, 1, passage_to, show_passage_numbers, translation)


def get_passage_as_list(passage_name, show_passage_numbers=True, translation='NIV'):
    """
    Gets all the text for a particular Bible passage from www.biblegateway.com, as a list of strings.
    :param passage_name: Name of the Bible passage which is valid when used on www.biblegateway.com
    :param show_passage_numbers: If True, passage numbers are provided at the start of each passage's text.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :return: Bible passage as a list with preserved line breaks
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
    return passage_list
