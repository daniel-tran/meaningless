from urllib.request import urlopen
import re

# This is a collection of helper methods used across the various modules.


def is_unsupported_translation(translation):
    """
    A helper function to determine if the provided translation code is supported

    :param translation: Translation code
    :type translation: str
    :return: True = the translation is not supported, False = the translation is supported
    :rtype: bool

    >>> is_unsupported_translation('msg')
    True
    >>> is_unsupported_translation('NIV')
    False
    """
    # These translations are particularly difficult to extract information from due to them using
    # non-conventional page layouts compared to other translations: 'MOUNCE', 'VOICE', 'MSG', 'PHILLIPS'
    return translation.upper() not in ['ASV', 'ESV', 'KJV', 'NASB', 'NIV', 'NKJV', 'NLT', 'NRSV', 'WEB']


def get_end_of_chapter():
    """
    A helper function to define the max. number of passages any chapter could possibly have.
    This is based on functionality present on Bible Gateway where a very large number is capped to the chapter's end.

    :return: A static number
    :rtype: int
    """
    return 9000


def get_chapter_count(book, translation='NIV'):
    """
    A helper function to return the number of chapter in a given book for a particular translation.

    :param book: Name of the book
    :type book: str
    :param translation: Translation code for the particular book. For example, 'NIV', 'ESV', 'NLT'
    :type translation: str
    :return: Number of chapters in the book. 0 usually means an invalid book or unsupported translation.
    :rtype: int

    >>> get_chapter_count('Ecclesiastes')
    12
    >>> get_chapter_count('Barnabas')
    0
    >>> get_chapter_count('Ecclesiastes', translation='msg')
    0
    >>> get_chapter_count('Song of Solomon')
    8
    >>> get_chapter_count('Psalms')
    150
    """
    # Standardise letter casing to help find the key easier
    book_name = book.title()

    if book_name == 'Song Of Solomon':
        # Song Of Songs has an alternate name
        book_name = 'Song Of Songs'
    elif book_name == 'Psalms':
        # Psalm and its plural variation are basically the same book, but prefer the singular variant
        book_name = 'Psalm'

    # This is the default mapping of books to their chapter counts
    chapter_count_mappings = {
        'Genesis': 50,
        'Exodus': 40,
        'Leviticus': 27,
        'Numbers': 36,
        'Deuteronomy': 34,
        'Joshua': 24,
        'Judges': 21,
        'Ruth': 4,
        '1 Samuel': 31,
        '2 Samuel': 24,
        '1 Kings': 22,
        '2 Kings': 25,
        '1 Chronicles': 29,
        '2 Chronicles': 36,
        'Ezra': 10,
        'Nehemiah': 13,
        'Esther': 10,
        'Job': 42,
        'Psalm': 150,
        'Proverbs': 31,
        'Ecclesiastes': 12,
        'Song Of Songs': 8,
        'Isaiah': 66,
        'Jeremiah': 52,
        'Lamentations': 5,
        'Ezekiel': 48,
        'Daniel': 12,
        'Hosea': 14,
        'Joel': 3,
        'Amos': 9,
        'Obadiah': 1,
        'Jonah': 4,
        'Micah': 7,
        'Nahum': 3,
        'Habakkuk': 3,
        'Zephaniah': 3,
        'Haggai': 2,
        'Zechariah': 14,
        'Malachi': 4,
        'Matthew': 28,
        'Mark': 16,
        'Luke': 24,
        'John': 21,
        'Acts': 28,
        'Romans': 16,
        '1 Corinthians': 16,
        '2 Corinthians': 13,
        'Galatians': 6,
        'Ephesians': 6,
        'Phillippians': 4,
        'Colossians': 4,
        '1 Thessalonians': 5,
        '2 Thessalonians': 3,
        '1 Timothy': 6,
        '2 Timothy': 4,
        'Titus': 3,
        'Philemon': 1,
        'Hebrews': 13,
        'James': 5,
        '1 Peter': 5,
        '2 Peter': 3,
        '1 John': 5,
        '2 John': 1,
        '3 John': 1,
        'Jude': 1,
        'Revelation': 22
    }
    # TODO Additional logic can be added here that changes chapter_count_mappings based on a given translation

    if book_name not in chapter_count_mappings.keys() or is_unsupported_translation(translation):
        return 0
    return chapter_count_mappings[book_name]


def get_page(url):
    """
    A helper function that returns the contents of a web page.

    :param url: Page URL to obtain
    :type url: str
    :return: Page contents. Raises an error if the web page could not be loaded for any reason.
    :rtype: object

    >>> get_page('https://www.biblegateway.com')
    b'<!DOCTYPE html>...'
    >>> get_page('https://www.something.com')
    Traceback (most recent call last):
    ...
    urllib.error.URLError: <urlopen error [WinError 10061] No connection could be made because the target \
machine actively refused it>
    """
    page = urlopen(url)
    content = page.read()
    page.close()
    return content


def superscript_numbers(text, remove_brackets=True):
    """
    A helper function that converts a string's numeric characters into their superscript Unicode variations

    :param text: String to process
    :type text: str
    :param remove_brackets: If True, removes bracket characters that would be considered non-standard formatting.
                            Mostly used to handle the case of empty passages such as Luke 17:36. Defaults to True.
    :type remove_brackets: bool
    :rtype: str

    >>> superscript_numbers('[0123456789]')
    '\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079'
    >>> superscript_numbers('Antidisestablishmentarianism')
    'Antidisestablishmentarianism'
    >>> superscript_numbers('[7]', False)
    '[\u2077]'
    """
    superscript_text = text
    if remove_brackets:
        # The strip method can't be relied on here, as the string itself can be space padded at times.
        # Using sequential replacements should be OK, unless there are more characters to handle.
        superscript_text = superscript_text.replace('[', '').replace(']', '').replace('(', '').replace(')', '')
    superscript_translation_table = superscript_text.maketrans('0123456789', '\u2070\u00b9\u00b2\u00b3\u2074\u2075'
                                                                             '\u2076\u2077\u2078\u2079')
    return superscript_text.translate(superscript_translation_table)


def remove_superscript_numbers_in_passage(text):
    """
    A helper function that removes all superscript numbers with optional trailing space from a given string.
    Mainly used to hide passage numbers in a given block of text.

    :param text: String to process
    :type text: str
    :return: String with the superscript numbers that have a trailing space removed
    :rtype: str

    >>> remove_superscript_numbers_in_passage('\u2070 \u00b9 \u00b2 \u00b3 \u2074 \u2075 \u2076 \u2077 \u2078 \u2079 ')
    ''
    >>> remove_superscript_numbers_in_passage('E=mc\u00b2')
    'E=mc'
    """
    return re.sub('[\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079]+\s{0,1}', '', text)


def get_capped_integer(number, min_value=1, max_value=100):
    """
    A helper function to limit an integer between an upper and lower bound

    :param number: Number to keep limited
    :type number: int
    :param min_value: Lowest possible value assigned when number is lower than this
    :type min_value: int
    :param max_value: Highest possible value assigned when number is larger than this
    :type max_value: int
    :return: Integer that adheres to min_value <= number <= max_value
    :rtype: int

    >>> get_capped_integer(42)
    42
    >>> get_capped_integer(0, min_value=7)
    7
    >>> get_capped_integer(42, max_value=7)
    7
    """
    return min(max(number, min_value), max_value)


def get_translation_language(translation):
    """
    A helper function to provide the language used in a given Bible translation

    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :type translation: str
    :return: Language used as a string. Empty string if the translation is not supported.
    :rtype: str

    >>> get_translation_language('NIV')
    'English'
    >>> get_translation_language('mounce')
    ''
    """
    translation = translation.title()
    if is_unsupported_translation(translation):
        return ''
    # TODO Currently, only English translations are supported. This could change in the future with other translations.
    return 'English'


def unicode_to_ascii_punctuation(text):
    """
    A helper function to convert certain punctuation characters from Unicode to ASCII

    :param text: String to process
    :type text: str
    :return: String with ASCII punctuation where relevant
    :rtype: str

    >>> unicode_to_ascii_punctuation('\u2018GG\u2019')
    "'GG'"
    >>> unicode_to_ascii_punctuation('\u201cG\u2014G\u201d')
    '"G-G"'
    >>> unicode_to_ascii_punctuation('GG')
    'GG'
    >>> unicode_to_ascii_punctuation('\u2070')
    '\u2070'
    """
    punctuation_map = text.maketrans('\u201c\u2018\u2014\u2019\u201d', '"\'-\'"')
    return text.translate(punctuation_map)

if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
