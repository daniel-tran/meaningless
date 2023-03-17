from bs4 import BeautifulSoup
from urllib.parse import urlencode
import sys
sys.path.append('../')
from meaningless.utilities import common


def find_keyword(keyword, translation, search_type):
    """
    Gets a list of passage matches using the Bible Gateway advanced search. This only returns the top 500 search
    results and will always search across all books.

    :param keyword: Search text
    :type keyword: str
    :param translation: Translation code. For example, 'NIV', 'ESV', 'NLT'
    :type translation: str
    :param search_type: Search mode. Should be set to one of the following strings:
                        'any' (match any word),
                        'all' (match all words),
                        'phrase' (match all words in given order)
    :type search_type: str
    :return: 2D array of data, where the first list contains the passage names of each match and the second
             list contains the passage contents for each item in the first list
    :rtype: list
    """
    source_site_params = urlencode({'version': translation, 'search': keyword, 'searchtype': search_type,
                                    'resultspp': '500'})
    soup = BeautifulSoup(common.get_page(
        f'https://www.biblegateway.com/quicksearch/?{source_site_params}'), 'html.parser')

    # Headers are for any paragraph headings present with the passage text.
    # Elements with the 'bible-item-extras' class are neighbouring hyperlinks that have the same parent element
    # as the passage text.
    removable_tags = soup.find_all('h3') + soup.find_all('div', {'class': 'bible-item-extras'})
    [tag.decompose() for tag in removable_tags]

    passage_titles = [tag.text for tag in soup.find_all('a', {'class': 'bible-item-title'})]
    passage_texts = [tag.text.strip() for tag in soup.find_all('div', {'class': 'bible-item-text'})]

    return [passage_titles, passage_texts]


if __name__ == "__main__":
    # Shows some results from Ecclesiastes
    # For some reason, 'Book of Isaiah' shows up as a match?
    print(str(find_keyword('everything is meaningless', 'NIV', 'all')))

    input('Next: Using phrase as search type')
    print(str(find_keyword('everything is meaningless', 'NIV', 'phrase')))

    input('Next: Using any as search type')
    print(str(find_keyword('everything is meaningless', 'NIV', 'any')))

    input('Next: Using invalid search type (defaults to type all)')
    print(str(find_keyword('meaningless', 'NIV', 'freed')))

    input('Next: No search results')
    print(str(find_keyword('Glove', 'NIV', 'any')))

    input('Next: Using HTML tag as search criteria')
    # Normally, this would redirect back to the homepage
    print(str(find_keyword('</span>', 'NIV', 'any')))

    input('Next: Using an invalid translation')
    print(str(find_keyword('meaningless', 'FREED', 'any')))

    input('Next: Empty search text')
    print(str(find_keyword('', 'NIV', 'any')))

    input('Next: Bugged input that shows HTML tags in the passage text')
    print(str(find_keyword('Lord.', 'NIV', 'any')))
