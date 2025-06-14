from urllib.request import urlopen
from urllib.error import URLError
from time import sleep
import re

# This is a collection of helper methods used across the various modules.

MEANINGLESS_VERSION = '1.2.0'
'''
The current version of the Meaningless library.
'''


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
    return translation.upper() not in BIBLE_TRANSLATIONS.keys()


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
    bible_translation = translation.upper()
    bible_book = book.title()

    if bible_book == 'Song Of Solomon':
        # Song Of Songs has an alternate name
        bible_book = 'Song Of Songs'
    elif bible_book == 'Psalms':
        # Psalm and its plural variation are basically the same book, but prefer the singular variant
        bible_book = 'Psalm'
    elif bible_book == 'Phillippians':
        # Most, if not all, translations use the spelling with one L but also accept the alternative spelling
        bible_book = 'Philippians'

    if bible_translation in BIBLE_TRANSLATIONS.keys() and \
       bible_book in BIBLE_TRANSLATIONS[bible_translation]['Books'].keys():
        return BIBLE_TRANSLATIONS[bible_translation]['Books'][bible_book]
    return 0


def get_page(url, retry_count=3, retry_delay=2):
    """
    A helper function that returns the contents of a web page.

    :param url: Page URL to obtain
    :type url: str
    :param retry_count: Number of attempts to resend the request if it fails after the first try
    :type retry_count: int
    :param retry_delay: Number of seconds to wait before retrying a request. This increases after every retry.
    :type retry_delay: int
    :return: Page contents. Raises an error if the web page could not be loaded for any reason.
    :rtype: str

    >>> get_page('https://www.biblegateway.com')
    b'<!DOCTYPE html>...'
    >>> get_page('https://www.randomwebsite.com', retry_count=0)
    Traceback (most recent call last):
    ...
    urllib.error.URLError: <urlopen error ...>
    >>> get_page('https://www.python.org/meaningless/', retry_count=2, retry_delay=1)
    Traceback (most recent call last):
    ...
    urllib.error.HTTPError: HTTP Error 404: Not Found
    """
    # Cap the values to ensure the function isn't suspended for an eternity, but still attempts at least once
    retries = get_capped_integer(retry_count, 0, 10)
    delay = get_capped_integer(retry_delay, 0, 30)
    delay_multiplier = 2
    # The extra addition to the range end is to account for the initial request
    for retry in range(0, retries + 1):
        try:
            with urlopen(url) as response:
                return response.read()
        except URLError as exception:
            if retry < retries:
                sleep(delay)
                delay *= delay_multiplier
                continue
            raise exception


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
    bible_translation = translation.upper()
    if bible_translation in BIBLE_TRANSLATIONS.keys():
        return BIBLE_TRANSLATIONS[bible_translation]['Language']
    return ''


def get_minimal_copyright_text(translation):
    """
    A helper function to provide the minimal recommended copyright text as per the Bible Gateway Terms of Use Agreement
    when quoting passages for non-commercial use.

    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :type translation: str
    :return: Minimal copyright text as a string. Empty string if the translation is not supported.
    :rtype: str

    >>> get_minimal_copyright_text('NIV')
    '(NIV)'
    >>> get_minimal_copyright_text('mounce')
    ''
    """
    bible_translation = translation.upper()
    if bible_translation in BIBLE_TRANSLATIONS.keys():
        return f'({translation})'
    return ''


def get_translation_copyright(translation):
    """
    A helper function to provide the copyright link for a given Bible translation

    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :type translation: str
    :return: Copyright link used as a string. Empty string if the translation is not supported.
    :rtype: str

    >>> get_translation_copyright('NIV')
    'https://www.biblegateway.com/versions/new-international-version-niv-bible/#copy'
    >>> get_translation_copyright('RVA')
    'https://www.biblegateway.com/versions/Reina-Valera-Antigua-RVA-Biblia/#copy'
    >>> get_translation_copyright('mounce')
    ''
    """
    bible_translation = translation.upper()
    if bible_translation in BIBLE_TRANSLATIONS.keys():
        return BIBLE_TRANSLATIONS[bible_translation]['Copyright']
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


def get_bible_data_for_language(language, mode=0):
    """
    A helper function to return miscellaneous Bible data for a particular supported language

    :param language: Language
    :type language: str
    :param mode: Numeric value corresponding to a specific data set. Defaults to 0.
                 0 = All information
                 1 = New Testament only
    :type mode: int
    :return: Dictionary containing Bible data relating to a particular supported language
    :rtype: dict

    >>> get_bible_data_for_language('English')
    {'Language': 'English', 'Books': {...'Ruth': 4...}
    >>> get_bible_data_for_language('English', mode=1)
    {'Language': 'English', 'Books': {'Matthew': 28...}
    >>> get_bible_data_for_language('Español')
    {'Language': 'Español', 'Books': {...'Rut': 4...}
    >>> get_bible_data_for_language('Saiyan')
    {'Language': 'Saiyan', 'Books': {}}
    """
    bible_language = language.title()

    # This is a general mapping of books and their total chapters applicable to most translations of a specific
    # language. Apocrypha books are not listed, partly because their total chapters vary between translations but
    # mostly due to these books not being officially supported.
    bible_book_mapping = {
        'English': {
            'OT': {
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
                'Malachi': 4
            },
            'NT': {
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
                'Philippians': 4,
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
        },
        'Español': {
            'OT': {
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
                'Malaquías': 4
            },
            'NT': {
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
        }
    }

    if bible_language in bible_book_mapping.keys():
        if mode == 1:
            bible_books = bible_book_mapping[bible_language]['NT']
        else:
            # Default to all information when the mode doesn't match one of the preset data sets
            bible_books = {**bible_book_mapping[bible_language]['OT'], **bible_book_mapping[bible_language]['NT']}
    else:
        # Unsupported language
        bible_books = {}

    return {
         'Language': bible_language,
         'Books': bible_books
    }


BIBLE_KEY_COPYRIGHT = 'Copyright'
BIBLE_TRANSLATIONS = {
    # English
    'AMP': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/Amplified-Bible-AMP/#copy',
    },
    'ASV': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/American-Standard-Version-ASV-Bible/#copy'
    },
    'AKJV': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/Authorized-King-James-Version-AKJV-Bible/#copy'
    },
    'BRG': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/BRG-Bible/#copy'
    },
    'CSB': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/Christian-Standard-Bible-CSB/#copy'
    },
    'EHV': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/Evangelical-Heritage-Version-EHV-Bible/#copy'
    },
    'ESV': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/English-Standard-Version-ESV-Bible/#copy'
    },
    'ESVUK': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/English-Standard-Version-Anglicised-ESV-Bible/#copy'
    },
    'GNV': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/1599-Geneva-Bible-GNV/#copy'
    },
    'GW': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/GODS-WORD-Translation-GW-Bible/#copy'
    },
    'ISV': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/International-Standard-Version-ISV-Bible/#copy'
    },
    'JUB': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/Jubilee-Bible-2000-JUB/#copy'
    },
    'KJV': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/King-James-Version-KJV-Bible/#copy'
    },
    'KJ21': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/21st-Century-King-James-Version-KJ21-Bible/#copy'
    },
    'LEB': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/Lexham-English-Bible-LEB/#copy'
    },
    'LSB': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/Legacy-Standard-Bible-LSB-Bible/#copy'
    },
    'MEV': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/Modern-English-Version-MEV-Bible/#copy'
    },
    'NASB': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/New-American-Standard-Bible-NASB/#copy'
    },
    'NASB1995': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/New-American-Standard-Bible-NASB1995/#copy'
    },
    'NET': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/New-English-Translation-NET-Bible/#copy'
    },
    'NIV': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/new-international-version-niv-bible/#copy'
    },
    'NIVUK': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/New-International-Version-UK-NIVUK-Bible/#copy'
    },
    'NKJV': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/New-King-James-Version-NKJV-Bible/#copy'
    },
    'NLT': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/New-Living-Translation-NLT-Bible/#copy'
    },
    'NLV': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/New-Life-Version-NLV-Bible/#copy'
    },
    'NMB': {
        **get_bible_data_for_language('English', mode=1),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/New-Matthew-Bible-NMB/#copy'
    },
    'NOG': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/Names-of-God-NOG-Bible/#copy'
    },
    'NRSV': {
        **get_bible_data_for_language('English'),  # Contains Apocrypha books that are currently omitted,
        # If you try to visit https://www.biblegateway.com/versions/New-Revised-Standard-Version-NRSV-Bible/#copy
        # you will be redirected to the NRSVUE translation
        BIBLE_KEY_COPYRIGHT:
            'https://www.biblegateway.com/versions/New-Revised-Standard-Version-Updated-Edition-NRSVue-Bible/#copy'
    },
    'NRSVUE': {
        **get_bible_data_for_language('English'),  # Contains Apocrypha books that are currently omitted
        BIBLE_KEY_COPYRIGHT:
            'https://www.biblegateway.com/versions/New-Revised-Standard-Version-Updated-Edition-NRSVue-Bible/#copy'
    },
    'RSV': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/Revised-Standard-Version-RSV-Bible/#copy'
    },
    'WEB': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/World-English-Bible-WEB/#copy'
    },
    'YLT': {
        **get_bible_data_for_language('English'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/Youngs-Literal-Translation-YLT-Bible/#copy'
    },
    # Spanish
    'RVA': {
        **get_bible_data_for_language('Español'),
        BIBLE_KEY_COPYRIGHT: 'https://www.biblegateway.com/versions/Reina-Valera-Antigua-RVA-Biblia/#copy'
    }
}
'''
The mapping of supported translations and associated Bible data, excluding Apocrypha information. For simplicity, all
book names use their common variant (e.g. 'Song Of Songs' instead of 'Song Of Solomon').
'''

if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
