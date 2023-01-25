from bs4 import BeautifulSoup
import re
import sys
sys.path.append('../')
from meaningless.utilities import common

# Credit to A. Baker, who wrote the original logic and provided written permission to adapt it


def get_online_chapter_list(translation, book_name):
    """
    Gets all available chapter numbers for a given book.

    :param translation: Translation code. For example, 'NIV', 'ESV', 'NLT'
    :type translation: str
    :param book_name: Name of the book
    :type book_name: str
    :return: List of numeric strings corresponding to the chapter numbers available in the specified book
    :rtype: list
    """

    switch = {
        # List of English Translations from https://www.biblegateway.com/versions/
        # Will need manually updated as translations are added/removed from their website
        'AKJV': 'Authorized-King-James-Version-AKJV-Bible',
        'AMP': 'Amplified-Bible-AMP',
        'AMPC': 'Amplified-Bible-Classic-Edition-AMPC',
        'ASV': 'American-Standard-Version-ASV-Bible',
        'BRG': 'BRG-Bible',
        'CEB': 'Common-English-Bible-CEB',
        'CEV': 'Contemporary-English-Version-CEV-Bible',
        'CJB': 'Complete-Jewish-Bible-CJB',
        'CSB': 'Christian-Standard-Bible-CSB',
        'DARBY': 'Darby-Translation-Bible',
        'DLNT': 'Disciples-Literal-New-Testament-DLNT',
        'DRA': 'Douay-Rheims-1899-American-Edition-DRA-Bible',
        'EHV': 'Evangelical-Heritage-Version-EHV-Bible',
        'ERV': 'Easy-to-Read-Version-ERV-Bible',
        'ESV': 'English-Standard-Version-ESV-Bible',
        'ESVUK': 'English-Standard-Version-Anglicised-ESV-Bible',
        'EXB': 'Expanded-Bible-EXB',
        'GNT': 'Good-News-Translation-GNT-Bible',
        'GNV': '1599-Geneva-Bible-GNV',
        'GW': 'GODS-WORD-Translation-GW-Bible',
        'HCSB': 'Holman-Christian-Standard-Bible-HCSB',
        'ICB': 'International-Childrens-Bible-ICB',
        'ISV': 'International-Standard-Version-ISV-Bible',
        'JUB': 'Jubilee-Bible-2000-JUB',
        'KJ21': '21st-Century-King-James-Version-KJ21-Bible',
        'KJV': 'King-James-Version-KJV-Bible',
        'LEB': 'Lexham-English-Bible-LEB',
        'MEV': 'Modern-English-Version-MEV-Bible',
        'MOUNCE': 'Mounce-Reverse-Interlinear-New-Testament',
        'MSG': 'Message-MSG-Bible',
        'NABRE': 'New-American-Bible-Revised-Edition-NABRE-Bible',
        'NASB': 'New-American-Standard-Bible-NASB',
        'NASB1995': 'New-American-Standard-Bible-NASB1995',
        'NCB': 'New-Catholic-Bible-NCB-Bible',
        'NCV': 'New-Century-Version-NCV-Bible',
        'NET': 'New-English-Translation-NET-Bible',
        'NIRV': 'New-International-Readers-Version-NIRV-Bible',
        'NIV': 'New-International-Version-NIV-Bible',
        'NIVUK': 'New-International-Version-UK-NIVUK-Bible',
        'NKJV': 'New-King-James-Version-NKJV-Bible',
        'NLT': 'New-Living-Translation-NLT-Bible',
        'NLV': 'New-Life-Version-NLV-Bible',
        'NMB': 'New-Matthew-Bible-NMB',
        'NOG': 'Names-of-God-NOG-Bible',
        'NRSV': 'New-Revised-Standard-Version-NRSV-Bible',
        'NRSVUE': 'New-Revised-Standard-Version-Updated-Edition-NRSVue-Bible',
        'NRSVA': 'New-Revised-Standard-Version-Anglicised-NRSVA-Bible',
        'NRSVCE': 'New-Revised-Standard-Version-Anglicised-Catholic-Edition-NRSVACE-Bible',
        'NTE': 'New-Testament-for-Everyone-NTE',
        'OJB': 'Orthodox-Jewish-Bible-OJB',
        'PHILLIPS': 'JB-Phillips-New-Testament',
        'RGT': 'Revised-Geneva-Translation-RGT-Bible',
        'RSV': 'Revised-Standard-Version-RSV-Bible',
        'RSVCE': 'Revised-Standard-Version-Catholic-Edition-RSVCE-Bible',
        'TLB': 'The-Living-Bible-TLB',
        'TLV': 'Tree-of-Life-Version-TLV-Bible',
        'TPT': 'The-Passion-Translation-TPT-Bible',  # No longer recognised on Bible Gateway
        'VOICE': 'The-Voice-Bible',
        'WE': 'Worldwide-English-New-Testament-WE',
        'WEB': 'World-English-Bible-WEB',
        'WYC': 'Wycliffe-Bible-WYC',
        'YLT': 'Youngs-Literal-Translation-YLT-Bible'
    }

    # Look up the translation in the dictionary and return an empty array if not found
    version_string = switch.get(translation)
    if not version_string:
        return []

    url = f'https://www.biblegateway.com/versions/{version_string}/#booklist'

    # There's a match, so download the page and search it for the requested book
    soup = BeautifulSoup(common.get_page(url), 'html.parser')

    # The spans inside the chapter's td complicate things - remove them
    [span.decompose() for span in soup.find_all('span')]

    # Search for the book_name and return [] if not found
    found_book_td = soup.find('td', class_='book-name', string=re.compile(book_name))
    if not found_book_td:
        return []

    chapter_list = []
    # Move 2 siblings over from the found td to the rightmost td,
    # and loop through the text of each link (chapter number)
    [chapter_list.append(chapter_num) for chapter_num in found_book_td.next_sibling.next_sibling.stripped_strings]

    return chapter_list


if __name__ == "__main__":
    # 'BOB' is not a valid translation - should return an empty array
    print('1. (BOB, Genesis, Expected: 0)\n  ' + str(get_online_chapter_list('BOB', 'Genesis')))
    # []
    
    # Malachi in NIV has 4 chapters
    print('2. (NIV, Malachi, Expected: 4)\n  ' + str(get_online_chapter_list('NIV', 'Malachi')))
    # ['1', '2', '3', '4']
    
    # Malachi in CJB only has 3 chapters
    print('3. (CJB, Malachi, Expected: 3)\n  ' + str(get_online_chapter_list('CJB', 'Malachi')))
    # ['1', '2', '3']
    
    # 'Tobit' does not exist in NIV
    print('4. (NIV, Tobit, Expected: 0)\n  ' + str(get_online_chapter_list('NIV', 'Tobit')))
    # []
    
    # 'Tobit' in CEB has 14 chapters
    print('5. (CEB, Tobit, Expected: 14)\n  ' + str(get_online_chapter_list('CEB', 'Tobit')))
    # ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']
    
    # Esther in NIV has 10 chapters
    print('6. (NIV, Esther, Expected: 10)\n  ' + str(get_online_chapter_list('NIV', 'Esther')))
    # ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    
    # Esther in NCB only has 9 chapters
    print('7. (NCB, Esther, Expected: 9)\n  ' + str(get_online_chapter_list('NCB', 'Esther')))
    # ['Intro', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # Intro appears to be a special case, link format is:
    # https://www.biblegateway.com/passage/intro/?search=Esther&version=NCB
    
    # Additions to Esther in WYC does not start with chapter 1!
    print('8. (WYC, Additions to Esther, Expected: 10)\n  ' +
          str(get_online_chapter_list('WYC', 'Additions to Esther')))
    # ['10', '11', '12', '13', '14', '15', '16']
    
    # TPT is no longer recognised as a valid translation
    print('8. (TPT, Jonah, Expected: 11)\n  ' + str(get_online_chapter_list('TPT', 'Jonah')))
