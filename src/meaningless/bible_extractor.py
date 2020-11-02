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


def __superscript_numbers(text):
    """
    A helper function that converts a string's numeric characters into their superscript Unicode variations

    >>> __superscript_numbers('0123456789')
    '\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079'
    >>> __superscript_numbers('Antidisestablishmentarianism')
    'Antidisestablishmentarianism'
    """
    return text.replace('0', '\u2070').replace('1', '\u00b9').replace('2', '\u00b2').replace('3', '\u00b3') \
               .replace('4', '\u2074').replace('5', '\u2075').replace('6', '\u2076').replace('7', '\u2077') \
               .replace('8', '\u2078').replace('9', '\u2079')


def get_passage(passage_name):
    """
    Gets all the text for a particular Bible passage from www.biblegateway.com
    Keep in mind that this logic will likely break when the page structure of said site is changed.
    :param passage_name: Name of the Bible passage which is valid when used on www.biblegateway.com
    :return: Bible passage as a string with preserved line breaks
    """
    translation = 'NIV'
    # Use the printer-friendly view since there are fewer page elements to load and process
    source_site_params = urlencode({'version': translation, 'search': passage_name, 'interface': 'print'})
    source_site = 'https://www.biblegateway.com/passage/?{0}'.format(source_site_params)
    soup = BeautifulSoup(__get_page(source_site), 'html.parser')

    for br in soup.find_all('br'):
        # <br> tags will naturally be ignored when getting text
        br.replace_with('\n')
    for h1 in soup.find_all('h1'):
        # Ignore passage display
        h1.decompose()
    for h3 in soup.find_all('h3'):
        # Ignore section headings
        h3.decompose()
    for h4 in soup.find_all('h4'):
        # Ignore subsection headings, such as those in Ezekiel 40
        h4.decompose()
    for readFullChapter in soup.find_all('a', {'class': 'full-chap-link'}):
        # Ignore the "Read Full Chapter" text, which is carefully embedded within the passage
        readFullChapter.decompose()
    for crossReference in soup.find_all('sup', {'class': 'crossreference'}):
        # Ignore cross references
        crossReference.decompose()
    for chapter_num in soup.find_all('span', {'class': 'chapternum'}):
        # Convert chapter numbers into new lines
        chapter_num.replace_with('\n')
    for sup in soup.find_all('sup', {'class': 'versenum'}):
        # Preserve superscript verse numbers by using their Unicode counterparts
        sup.string = __superscript_numbers(sup.text)
    for footnote in soup.find_all('sup', {'class': 'footnote'}):
        # Ignore in-line footnotes
        footnote.decompose()
    for blacklisted_class in soup.find_all('div', {'class': re.compile(
            'footnotes|dropdowns|crossrefs|passage-other-trans')}):
        # Ignore the footer area, which is composed of several main tags
        blacklisted_class.decompose()
    for td in soup.find_all('td', {'class': 'right'}):
        # Some verses such as Nehemiah 7:30 - 42 store text in a <table> instead of <p>, which means
        # spacing is not preserved when collecting the text. Therefore, a space is manually injected
        # into the right cell's text to stop it from joining the left cell's text.
        # TODO: If a verse with >2 columns is found, this WILL need to be updated to be more dynamic
        td.string = ' {0}'.format(td.text)
    for p in soup.find_all('p'):
        # Preserve paragraph spacing
        # Use p.string because p.text is read-only
        # THIS MUST BE THE LAST PROCESSING STEP because doing this earlier interferes with other replacements
        p.string = '\n{0}'.format(p.text)
    all_text = soup.find('div', {'class': 'version-{0}'.format(translation)})

    # Don't collect contents from an invalid verse, since they do not exist.
    # However, the main verse slide still has this passage name, so that
    # an off-screen passage is still possible.
    if not all_text:
        print('WARNING: "{0}" is not a valid passage.'.format(passage_name))
        return ''

    # Do any final touch-ups to the passage contents
    return all_text.text.strip()

if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
