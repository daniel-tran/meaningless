from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlencode
import re


def __get_page(url):
    """
    A helper function that returns the contents of a web page.

    >>> __get_page('https://www.biblegateway.com')
    b'<!DOCTYPE html>...'
    >>> __get_page('https://www.something.com')
    Traceback (most recent call last):
    ...
    urllib.error.URLError: <urlopen error [WinError 10061] No connection could be made because the target \
machine actively refused it>
    """
    page = urlopen(url)
    content = page.read()
    page.close()
    return content


def __superscript_numbers(text, normalise_empty_passage=True):
    """
    A helper function that converts a string's numeric characters into their superscript Unicode variations
    :param text: String to process
    :param normalise_empty_passage: If True, performs additional replacements to normalise other characters that would
                                    be considered non-standard formatting. Mostly used to handle the case of empty
                                    passages such as Luke 17:36.

    >>> __superscript_numbers('[0123456789]')
    '\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079'
    >>> __superscript_numbers('Antidisestablishmentarianism')
    'Antidisestablishmentarianism'
    >>> __superscript_numbers('[7]', False)
    '[\u2077]'
    """
    superscript_text = text
    if normalise_empty_passage:
        superscript_text = text.replace('[', '').replace(']', '')
    return superscript_text.replace('0', '\u2070').replace('1', '\u00b9').replace('2', '\u00b2') \
                           .replace('3', '\u00b3').replace('4', '\u2074').replace('5', '\u2075') \
                           .replace('6', '\u2076').replace('7', '\u2077').replace('8', '\u2078').replace('9', '\u2079')


def __is_unsupported_translation(translation):
    """
    A helper function to determine if the provided translation code is supported
    :param translation: Translation code
    :return: True = the translation is not supported, False = the translation is supported

    >>> __is_unsupported_translation('msg')
    True
    >>> __is_unsupported_translation('NIV')
    False
    """
    return translation.upper() in ['MOUNCE', 'VOICE', 'MSG', 'PHILLIPS']


def get_passage(passage_name, passage_separator='', show_passage_numbers=True, translation='NIV'):
    """
    Gets all the text for a particular Bible passage from www.biblegateway.com
    Keep in mind that this logic will likely break when the page structure of said site is changed.
    :param passage_name: Name of the Bible passage which is valid when used on www.biblegateway.com
    :param passage_separator: An optional string added to the front of a passage (placed before the passage number).
                              Mainly used to separate passages in a more customised way.
    :param show_passage_numbers: If True, passage numbers are provided at the start of each passage's text.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :return: Bible passage as a string with preserved line breaks
    """
    # Some translations are very tricky to extract passages from, and currently, so specific extraction logic for these
    # translations should not be introduced until they need to be supported.
    translation = translation.upper()
    if __is_unsupported_translation(translation):
        print('WARNING: "{0}" is not a supported translation.'.format(translation))
        return ''

    # Use the printer-friendly view since there are fewer page elements to load and process
    source_site_params = urlencode({'version': translation, 'search': passage_name, 'interface': 'print'})
    source_site = 'https://www.biblegateway.com/passage/?{0}'.format(source_site_params)
    soup = BeautifulSoup(__get_page(source_site), 'html.parser')

    # Don't collect contents from an invalid verse, since they do not exist.
    # A fail-fast approach can be taken by checking for certain indicators of invalidity.
    if not soup.find('div', {'class': 'passage-content'}):
        print('WARNING: "{0}" is not a valid passage.'.format(passage_name))
        return ''

    # Compile the list of tags to remove from the parsed web page, corresponding to the following elements:
    # h1
    #    - Ignore passage display
    # h3
    #    - Ignore section headings
    # h4
    #    - Ignore subsection headings, such as those in Ezekiel 40
    # a with 'full-chap-link' class
    #    - Ignore the "Read Full Chapter" text, which is carefully embedded within the passage
    # sup with 'crossreference' class
    #    - Ignore cross references
    # sup with 'footnote' class
    #    - Ignore in-line footnotes
    # div with one of the 'footnotes', 'dropdowns', 'crossrefs', 'passage-other-trans' classes
    #    - Ignore the footer area, which is composed of several main tags
    removable_tags = soup.find_all(re.compile('^h1$|^h3$|^h4$')) \
        + soup.find_all('a', {'class': 'full-chap-link'}) \
        + soup.find_all('sup', {'class': re.compile('^crossreference$|^footnote$')}) \
        + soup.find_all('div', {'class': re.compile('^footnotes$|^dropdowns$|^crossrefs$|^passage-other-trans$')})
    [tag.decompose() for tag in removable_tags]

    # <br> tags will naturally be ignored when getting text
    [br.replace_with('\n') for br in soup.find_all('br')]
    # Convert chapter numbers into new lines
    [chapter_num.replace_with('\n') for chapter_num in soup.find_all('span', {'class': 'chapternum'})]
    # Preserve superscript verse numbers by using their Unicode counterparts
    # Add in the custom passage separator as well while access to the verse numbers is still available
    [sup.replace_with('{0}{1}'.format(passage_separator, __superscript_numbers(sup.text)))
        for sup in soup.find_all('sup', {'class': 'versenum'})]
    # Some verses such as Nehemiah 7:30 - 42 store text in a <table> instead of <p>, which means
    # spacing is not preserved when collecting the text. Therefore, a space is manually injected
    # into the right cell's text to stop it from joining the left cell's text.
    # TODO: If a verse with >2 columns is found, this WILL need to be updated to be more dynamic
    [td.replace_with(' {0}'.format(td.text)) for td in soup.find_all('td', {'class': 'right'})]
    # Preserve paragraph spacing by manually pre-pending a new line
    # THIS MUST BE THE LAST PROCESSING STEP because doing this earlier interferes with other replacements
    [p.replace_with('\n{0}'.format(p.text)) for p in soup.find_all('p')]

    all_text = soup.find('div', {'class': 'passage-content'}).text

    # Remove all superscript numbers if the passage numbers should be hidden
    if not show_passage_numbers:
        all_text = re.sub('[\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079]+\s', '', all_text)
    # EXB has in-line notes which are usually enclosed within brackets, and should not be displayed.
    # If the in-line note is simply decomposed, removing the associated space is much more difficult.
    # Thus, the in-line note text is removed at the end, when the function is strictly handling the passage text
    # to eliminate both the in-line note and its space in an easy manner.
    if translation == 'EXB':
        all_text = re.sub('\s\[.+?\]', '', all_text)
    # Do any final touch-ups to the passage contents
    return all_text.strip().replace('\xa0', ' ')


def get_passage_as_list(passage_name, show_passage_numbers=True, translation='NIV'):
    """
    Gets all the text for a particular Bible passage from www.biblegateway.com, as a list of strings.
    Unlike get_passage(), the superscript passage numbers are NOT preserved.
    :param passage_name: Name of the Bible passage which is valid when used on www.biblegateway.com
    :param show_passage_numbers: If True, passage numbers are provided at the start of each passage's text.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :return: Bible passage as a list with preserved line breaks
    """
    # Use a string that is guaranteed to not occur anywhere in the Bible in any translation.
    # This now becomes the splitting string so that superscript passage numbers can be preserved.
    passage_separator = '-_-'
    passage_text = get_passage(passage_name, passage_separator=passage_separator,
                               show_passage_numbers=show_passage_numbers, translation=translation)

    passage_list = re.split(passage_separator, passage_text)
    # Remove the first empty item
    if len(passage_list[0]) <= 0:
        passage_list.pop(0)
    return passage_list

if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
