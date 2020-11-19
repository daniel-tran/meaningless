from urllib.request import urlopen
from urllib.parse import urlencode
import re

# This is a collection of helper methods used across the various modules.


def is_unsupported_translation(translation):
    """
    A helper function to determine if the provided translation code is supported
    :param translation: Translation code
    :return: True = the translation is not supported, False = the translation is supported

    >>> is_unsupported_translation('msg')
    True
    >>> is_unsupported_translation('NIV')
    False
    """
    # These translations are particularly difficult to extract information from due to them using
    # non-conventional page layouts compared to other translations: 'MOUNCE', 'VOICE', 'MSG', 'PHILLIPS'
    return translation.upper() not in ['NIV', 'NASB', 'NKJV', 'NRSV', 'ESV', 'WEB', 'NLT']


def get_page(url):
    """
    A helper function that returns the contents of a web page.

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


def superscript_numbers(text, normalise_empty_passage=True):
    """
    A helper function that converts a string's numeric characters into their superscript Unicode variations
    :param text: String to process
    :param normalise_empty_passage: If True, performs additional replacements to normalise other characters that would
                                    be considered non-standard formatting. Mostly used to handle the case of empty
                                    passages such as Luke 17:36.

    >>> superscript_numbers('[0123456789]')
    '\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079'
    >>> superscript_numbers('Antidisestablishmentarianism')
    'Antidisestablishmentarianism'
    >>> superscript_numbers('[7]', False)
    '[\u2077]'
    """
    superscript_text = text
    if normalise_empty_passage:
        superscript_text = text.replace('[', '').replace(']', '').replace('(', '').replace(')', '')
    return superscript_text.replace('0', '\u2070').replace('1', '\u00b9').replace('2', '\u00b2') \
                           .replace('3', '\u00b3').replace('4', '\u2074').replace('5', '\u2075') \
                           .replace('6', '\u2076').replace('7', '\u2077').replace('8', '\u2078').replace('9', '\u2079')


def remove_superscript_numbers_in_passage(text):
    """
    A helper function that removes all superscript numbers with a trailing space from a given string.
    Mainly used to hide passage numbers in a given block of text.
    :param text: String to process
    :return: String with the superscript numbers that have a trailing space removed

    >>> remove_superscript_numbers_in_passage('\u2070 \u00b9 \u00b2 \u00b3 \u2074 \u2075 \u2076 \u2077 \u2078 \u2079 ')
    ''
    >>> remove_superscript_numbers_in_passage('E=mc\u00b2')
    'E=mc\u00b2'
    """
    return re.sub('[\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079]+\s', '', text)


def get_capped_integer(number, min_value=1, max_value=100):
    """
    A helper function to limit an integer between an upper and lower bound
    :param number: Number to keep limited
    :param min_value: Lowest possible value assigned when number is lower than this
    :param max_value: Highest possible value assigned when number is larger than this
    :return: Integer that adheres to min_value <= number <= max_value

    >>> get_capped_integer(42)
    42
    >>> get_capped_integer(0, min_value=7)
    7
    >>> get_capped_integer(42, max_value=7)
    7
    """
    return min(max(number, min_value), max_value)


if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
