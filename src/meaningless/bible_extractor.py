from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlencode
import re
from meaningless.utilities import common


def get_online_passage(book, chapter, passage, passage_separator='', show_passage_numbers=True, translation='NIV'):
    """
    Gets a single passage from the Bible Gateway site
    :param book: Name of the book
    :param chapter: Chapter number
    :param passage: Passage number
    :param passage_separator: An optional string added to the front of a passage (placed before the passage number).
                              Mainly used to separate passages in a more customised way.
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :return: The passage as text. Empty string if the passage is invalid.
    """
    search = '{0} {1}:{2}'.format(book, chapter, passage)
    return get_passage(search, passage_separator, show_passage_numbers, translation)


def get_online_passages(book, chapter, passage_from, passage_to, passage_separator='', show_passage_numbers=True,
                        translation='NIV'):
    """
    Gets a range of passages of the same chapter from the Bible Gateway site
    :param book: Name of the book
    :param chapter: Chapter number
    :param passage_from: First passage number to get
    :param passage_to: Last passage number to get
    :param passage_separator: An optional string added to the front of a passage (placed before the passage number).
                              Mainly used to separate passages in a more customised way.
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :return: The passage as text. Empty string if the passage is invalid.
    """
    search = '{0} {1}:{2} - {3}'.format(book, chapter, passage_from, passage_to)
    return get_passage(search, passage_separator, show_passage_numbers, translation)


def get_online_chapter(book, chapter, passage_separator='', show_passage_numbers=True, translation='NIV'):
    """
    Gets a single chapter from the Bible Gateway site
    :param book: Name of the book
    :param chapter: Chapter number
    :param passage_separator: An optional string added to the front of a passage (placed before the passage number).
                              Mainly used to separate passages in a more customised way.
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :return: The passage as text. Empty string if the passage is invalid.
    """
    search = '{0} {1}'.format(book, chapter)
    return get_passage(search, passage_separator, show_passage_numbers, translation)


def get_online_chapters(book, chapter_from, chapter_to, passage_separator='', show_passage_numbers=True,
                        translation='NIV'):
    """
    Gets a range of passages from a specified chapters selection from the Bible Gateway site.
    This function stays within the passage contents max. limit by making incremental requests
    for each chapter's contents, and combines it into a single multi-line string.
    As such, the output is not guaranteed to be the same as invoking get_passage() with the same search string,
    however the output is going to be similar to contents provided by the YAML extractor.
    :param book: Name of the book
    :param chapter_from: First chapter number to get
    :param chapter_to: Last chapter number to get
    :param passage_separator: An optional string added to the front of a passage (placed before the passage number).
                              Mainly used to separate passages in a more customised way.
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :return: The passage as text. Empty string if the passage is invalid.
    """
    # Retrieve chapters one by one to stay within the max. text limit when requesting for passages.
    # Add 1 to the end of the range, since the last chapter is also to be included.
    chapters = [get_online_chapter(book, chapter, passage_separator, show_passage_numbers, translation)
                for chapter in range(chapter_from, chapter_to + 1)]
    return '\n'.join(chapters)


def get_online_passage_range(book, chapter_from, passage_from, chapter_to, passage_to, passage_separator='',
                             show_passage_numbers=True, translation='NIV'):
    """
    Gets a range of passages from one specific passage to another passage from the Bible Gateway site.
    This function stays within the passage contents max. limit by making incremental requests
    for each chapter's contents, and combines it into a single multi-line string.
    As such, the output is not guaranteed to be the same as invoking get_passage() with the same search string,
    however the output is going to be similar to contents provided by the YAML extractor.
    :param book: Name of the book
    :param chapter_from: First chapter number to get
    :param passage_from: First passage number to get in the first chapter
    :param chapter_to: Last chapter number to get
    :param passage_to: Last passage number to get in the last chapter
    :param passage_separator: An optional string added to the front of a passage (placed before the passage number).
                              Mainly used to separate passages in a more customised way.
    :param show_passage_numbers: If True, any present passage numbers are preserved.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :return: The passage as text. Empty string if the passage is invalid.
    """
    # Defer to a simpler alternative function when sourcing passages from the same chapter
    if chapter_from == chapter_to:
        return get_online_passages(book, chapter_from, passage_from, passage_to, passage_separator,
                                   show_passage_numbers, translation)

    # Get the partial section of the first chapter being requested, omitting some initial passages
    initial_chapter = get_online_passages(book, chapter_from, passage_from, common.get_end_of_chapter(),
                                          passage_separator, show_passage_numbers, translation)
    # Get the partial section of the last chapter being requested, omitting some trailing passages
    final_chapter = get_online_passages(book, chapter_to, 1, passage_to, passage_separator,
                                        show_passage_numbers, translation)
    # Get all the chapters in between the initial and final chapters (exclusive since they have been pre-fetched).
    # Sandwich those chapters between the first and last pre-fetched chapters to combine all the passage data.
    chapters = [initial_chapter] + \
               [get_online_chapter(book, chapter, passage_separator, show_passage_numbers, translation)
                for chapter in range(chapter_from + 1, chapter_to)] + [final_chapter]
    return '\n'.join(chapters)


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
    if common.is_unsupported_translation(translation):
        print('WARNING: "{0}" is not a supported translation.'.format(translation))
        return ''

    # Use the printer-friendly view since there are fewer page elements to load and process
    source_site_params = urlencode({'version': translation, 'search': passage_name, 'interface': 'print'})
    source_site = 'https://www.biblegateway.com/passage/?{0}'.format(source_site_params)
    soup = BeautifulSoup(common.get_page(source_site), 'html.parser')

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
    # span with 'selah' class
    #    - Ignore explicit Psalm interludes in the translations such as NLT and CEB
    # selah
    #    - Ignore explicit Psalm interludes in the translations such as HCSB
    # p with 'translation-note' class
    #    - Ignore explicit translation notes in translations such as ESV
    removable_tags = soup.find_all(re.compile('^h1$|^h3$|^h4$')) \
        + soup.find_all('a', {'class': 'full-chap-link'}) \
        + soup.find_all('sup', {'class': re.compile('^crossreference$|^footnote$')}) \
        + soup.find_all('div', {'class': re.compile('^footnotes$|^dropdowns$|^crossrefs$|^passage-other-trans$')}) \
        + soup.find_all('span', {'class': 'selah'}) \
        + soup.find_all('selah') \
        + soup.find_all('p', {'class': 'translation-note'})
    [tag.decompose() for tag in removable_tags]

    # <br> tags will naturally be ignored when getting text
    [br.replace_with('\n') for br in soup.find_all('br')]
    # Convert chapter numbers into new lines
    [chapter_num.replace_with('\n') for chapter_num in soup.find_all('span', {'class': 'chapternum'})]
    # Preserve superscript verse numbers by using their Unicode counterparts
    # Add in the custom passage separator as well while access to the verse numbers is still available
    [sup.replace_with('{0}{1}'.format(passage_separator, common.superscript_numbers(sup.text)))
        for sup in soup.find_all('sup', {'class': 'versenum'})]
    # Some verses such as Nehemiah 7:30 - 42 store text in a <table> instead of <p>, which means
    # spacing is not preserved when collecting the text. Therefore, a space is manually injected
    # onto the end of the left cell's text to stop it from joining the right cell's text.
    # Note: Python "double colon" syntax for lists is used to retrieve items at every N interval including 0.
    # TODO: If a verse with >2 columns is found, this WILL need to be updated to be more dynamic
    [td.replace_with('{0} '.format(td.text)) for td in soup.find_all('td')[::2]]
    # Preserve paragraph spacing by manually pre-pending a new line
    # THIS MUST BE THE LAST PROCESSING STEP because doing this earlier interferes with other replacements
    [p.replace_with('\n{0}'.format(p.text)) for p in soup.find_all('p')]

    all_text = soup.find('div', {'class': 'passage-content'}).text

    # Remove all superscript numbers if the passage numbers should be hidden
    if not show_passage_numbers:
        all_text = common.remove_superscript_numbers_in_passage(all_text)
    # EXB has in-line notes which are usually enclosed within brackets, and should not be displayed.
    # If the in-line note is simply decomposed, removing the associated space is much more difficult.
    # Thus, the in-line note text is removed at the end, when the function is strictly handling the passage text
    # to eliminate both the in-line note and its space in an easy manner.
    if translation == 'EXB':
        all_text = re.sub('\s\[.+?\]', '', all_text)
    # Do any final touch-ups to the passage contents
    return all_text.strip().replace('\xa0', ' ')

if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    import doctest
    doctest.testmod(verbose=True, optionflags=doctest.ELLIPSIS)
