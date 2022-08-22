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
    return not is_supported_english_translation(translation) and not is_supported_spanish_translation(translation)


def is_supported_english_translation(translation):
    """
    A helper function to determine if the provided string is a supported English translation.

    :param translation: Translation code
    :type translation: str
    :return: True = the translation is not supported, False = the translation is supported
    :rtype: bool

    >>> is_supported_english_translation('NIV')
    True
    >>> is_supported_english_translation('RVA')
    False
    """
    return translation.upper() in ['ASV', 'AKJV', 'BRG', 'EHV', 'ESV', 'ESVUK', 'GNV', 'GW', 'ISV',
                                   'JUB', 'KJV', 'KJ21', 'LEB', 'MEV', 'NASB', 'NASB1995', 'NET',
                                   'NIV', 'NIVUK', 'NKJV', 'NLT', 'NLV', 'NOG', 'NRSV', 'NRSVUE', 'WEB', 'YLT']


def is_supported_spanish_translation(translation):
    """
    A helper function to determine if the provided string is a supported Spanish translation.

    :param translation: Translation code
    :type translation: str
    :return: True = the translation is not supported, False = the translation is supported
    :rtype: bool

    >>> is_supported_spanish_translation('RVA')
    True
    >>> is_supported_spanish_translation('NIV')
    False
    """
    return translation.upper() in ['RVA']


def is_matching_translation(translation1, translation2):
    """
    A helper function to compare two translation strings and determine if they are equivalent.
    This will also consider any applicable translation aliases.

    :param translation1: First translation code
    :type translation1: str
    :param translation2: Second translation code
    :type translation2: str
    :return: True = both translations are equivalent, False = the translations are different
    :rtype: bool

    >>> is_matching_translation('NIV', 'NIV')
    True
    >>> is_matching_translation('NlT', 'nLt')
    True
    >>> is_matching_translation('NLT', 'NIV')
    False
    >>> is_matching_translation('NIV ', 'NIV')
    False
    >>> is_matching_translation('NRSV', 'NRSVUE')
    True

    """
    translation_first = translation1.upper()
    translation_second = translation2.upper()
    aliases_nrsv = ['NRSV', 'NRSVUE']
    return translation_first == translation_second or \
        (translation_first in aliases_nrsv and translation_second in aliases_nrsv)


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
    A helper function to return the number of chapters in a given book for a particular translation.

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
    >>> get_chapter_count('Juan', 'RVA')
    21
    """
    if is_supported_english_translation(translation):
        return get_english_chapter_count(book)
    elif is_supported_spanish_translation(translation):
        return get_spanish_chapter_count(book)
    else:
        return 0


def get_english_chapter_count(book):
    """
    A helper function to return the number of chapters in a given book in the English version of the Bible.

    :param book: Name of the book
    :type book: str
    :return: Number of chapters in the book. 0 usually means an invalid book or unsupported translation.
    :rtype: int

    >>> get_english_chapter_count('Ecclesiastes')
    12
    >>> get_english_chapter_count('Barnabas')
    0
    >>> get_english_chapter_count('Song of Solomon')
    8
    >>> get_english_chapter_count('Psalms')
    150
    >>> get_english_chapter_count('Philippians')
    4
    """
    # Standardise letter casing to help find the key easier
    book_name = book.title()

    if book_name == 'Song Of Solomon':
        # Song Of Songs has an alternate name
        book_name = 'Song Of Songs'
    elif book_name == 'Psalms':
        # Psalm and its plural variation are basically the same book, but prefer the singular variant
        book_name = 'Psalm'
    elif book_name == 'Philippians':
        # Prefer the spelling variation with two L's, partly for backwards compatibility with previous versions
        book_name = 'Phillippians'

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
        'Revelation': 22,
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
    if book_name not in chapter_count_mappings.keys():
        return 0
    return chapter_count_mappings[book_name]


def get_spanish_chapter_count(book):
    """
    A helper function to return the number of chapters in a given book in the Spanish version of the Bible.

    :param book: Name of the book
    :type book: str
    :return: Number of chapters in the book. 0 means an invalid book.
    :rtype: int

    >>> get_spanish_chapter_count('Hechos')
    28
    >>> get_spanish_chapter_count('Ecclesiastes')
    0
    """
    # Standardise letter casing to help find the key easier
    book_name = book.title()

    # This is the default mapping of books to their chapter counts
    chapter_count_mappings = {
        'Génesis': 50,
        'Éxodo': 40,
        'Levítico': 27,
        'Números': 36,
        'Deuteronomio': 34,
        'Josué': 24,
        'Jueces': 21,
        'Rut': 4,
        '1 Samuel': 31,
        '2 Samuel': 24,
        '1 Reyes': 22,
        '2 Reyes': 25,
        '1 Crónicas': 29,
        '2 Crónicas': 36,
        'Esdras': 10,
        'Nehemías': 13,
        'Ester': 10,
        'Job': 42,
        'Salmos': 150,
        'Proverbios': 31,
        'Eclesiastés': 12,
        'Cantares': 8,
        'Isaías': 66,
        'Jeremías': 52,
        'Lamentaciones': 5,
        'Ezequiel': 48,
        'Daniel': 12,
        'Oseas': 14,
        'Joel': 3,
        'Amós': 9,
        'Abdías': 1,
        'Jonás': 4,
        'Miqueas': 7,
        'Nahúm': 3,
        'Habacuc': 3,
        'Sofonías': 3,
        'Hageo': 2,
        'Zacarías': 14,
        'Malaquías': 4,
        'Mateo': 28,
        'Marcos': 16,
        'Lucas': 24,
        'Juan': 21,
        'Hechos': 28,
        'Romanos': 16,
        '1 Corintios': 16,
        '2 Corintios': 13,
        'Gálatas': 6,
        'Efesios': 6,
        'Filipenses': 4,
        'Colosenses': 4,
        '1 Tesalonicenses': 5,
        '2 Tesalonicenses': 3,
        '1 Timoteo': 6,
        '2 Timoteo': 4,
        'Tito': 3,
        'Filemón': 1,
        'Hebreos': 13,
        'Santiago': 5,
        '1 Pedro': 5,
        '2 Pedro': 3,
        '1 Juan': 5,
        '2 Juan': 1,
        '3 Juan': 1,
        'Judas': 1,
        'Apocalipsis': 22
    }
    if book_name not in chapter_count_mappings.keys():
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
    >>> get_page('https://www.randomwebsite.com')
    Traceback (most recent call last):
    ...
    urllib.error.URLError: <urlopen error ...>
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
    '⁰¹²³⁴⁵⁶⁷⁸⁹'
    >>> superscript_numbers('Antidisestablishmentarianism')
    'Antidisestablishmentarianism'
    >>> superscript_numbers('[7]', False)
    '[⁷]'
    """
    superscript_text = text
    if remove_brackets:
        # The strip method can't be relied on here, as the string itself can be space padded at times.
        # Using sequential replacements should be OK, unless there are more characters to handle.
        superscript_text = superscript_text.replace('[', '').replace(']', '').replace('(', '').replace(')', '')
    superscript_translation_table = superscript_text.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
    return superscript_text.translate(superscript_translation_table)


def remove_superscript_numbers_in_passage(text):
    """
    A helper function that removes all superscript numbers with optional trailing space from a given string.
    Mainly used to hide passage numbers in a given block of text.

    :param text: String to process
    :type text: str
    :return: String with the superscript numbers that have a trailing space removed
    :rtype: str

    >>> remove_superscript_numbers_in_passage('⁰ ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹ ')
    ''
    >>> remove_superscript_numbers_in_passage('E=mc²')
    'E=mc'
    """
    return re.sub(r'[⁰¹²³⁴⁵⁶⁷⁸⁹]+\s?', '', text)


def get_capped_integer(number, min_value=1, max_value=100):
    """
    A helper function to limit an integer between an upper and lower bound

    :param number: Number to keep limited
    :type number: int or str
    :param min_value: Lowest possible value assigned when number is lower than this
    :type min_value: int or str
    :param max_value: Highest possible value assigned when number is larger than this
    :type max_value: int or str
    :return: Integer that adheres to min_value <= number <= max_value
    :rtype: int

    >>> get_capped_integer(42)
    42
    >>> get_capped_integer(0, min_value=7)
    7
    >>> get_capped_integer(42, max_value=7)
    7
    >>> get_capped_integer('0', min_value='7')
    7
    >>> get_capped_integer('42', max_value='7')
    7
    """
    return min(max(int(number), int(min_value)), int(max_value))


def dict_keys_to_sorted_list(keys):
    """
    A helper function that converts a dictionary's keys to a sorted list.

    :param keys: Dictionary keys
    :type keys: object
    :return: Dictionary keys casted as a sorted list
    :rtype: list

    >>> dict_keys_to_sorted_list({4: '', 2: '', 7: ''}.keys())
    [2, 4, 7]
    >>> dict_keys_to_sorted_list({'4': '', '2': '', '7': ''}.keys())
    ['2', '4', '7']
    """
    def key_sorting_function(key):
        # An inner sorting function that is primarily used for sorting numeric keys or strings of numeric characters.
        # TODO Sorting on string keys with actual alphabetic characters requires additional logic and doctests
        return int(key)

    sorted_keys = list(keys)
    sorted_keys.sort(key=key_sorting_function)
    return sorted_keys


def get_translation_language(translation):
    """
    A helper function to provide the language used in a given Bible translation

    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :type translation: str
    :return: Language used as a string. Empty string if the translation is not supported.
    :rtype: str

    >>> get_translation_language('NIV')
    'English'
    >>> get_translation_language('RVA')
    'Español'
    >>> get_translation_language('mounce')
    ''
    """
    translation = translation.title()
    if is_supported_english_translation(translation):
        return 'English'
    elif is_supported_spanish_translation(translation):
        return 'Español'
    else:
        return ''


def unicode_to_ascii_punctuation(text):
    """
    A helper function to convert certain punctuation characters from Unicode to ASCII

    :param text: String to process
    :type text: str
    :return: String with ASCII punctuation where relevant
    :rtype: str

    >>> unicode_to_ascii_punctuation('‘GG’')
    "'GG'"
    >>> unicode_to_ascii_punctuation('“G—G”')
    '"G-G"'
    >>> unicode_to_ascii_punctuation('GG')
    'GG'
    >>> unicode_to_ascii_punctuation('⁰')
    '⁰'
    """
    punctuation_map = text.maketrans('“‘—’”', '"\'-\'"')
    return text.translate(punctuation_map)


def cast_to_str_or_int(text, cast_to_str):
    """
    A helper function to convert a given input to either a string or an integer.

    :param text: Input text
    :type text: int or str
    :param cast_to_str: When True, input text is cast to a string. When False, input is cast to an integer.
    :type cast_to_str: bool
    :return: A string or integer representation of the input string
    :rtype: int (str if cast_to_str is True)

    >>> cast_to_str_or_int('Tri-Beam', True)
    'Tri-Beam'
    >>> cast_to_str_or_int('42', False)
    42
    >>> cast_to_str_or_int('42', True)
    '42'
    >>> cast_to_str_or_int(42, False)
    42
    >>> cast_to_str_or_int(42, True)
    '42'
    >>> cast_to_str_or_int('Tri-Beam', False)
    'Tri-Beam'
    """
    if not cast_to_str:
        # Input text that cannot be cast to an integer are instead cast to a string
        try:
            return int(text)
        except ValueError:
            pass
    return str(text)


if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
