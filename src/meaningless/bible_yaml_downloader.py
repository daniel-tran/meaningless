import os
import meaningless.bible_extractor
from ruamel.yaml import YAML

# Storing the value of each book with its total number of chapters.
# This assumes the default books and chapter counts in well-known Bible translations such as NIV and ESV.
__chapter_count_mappings = {
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


def yaml_download(book, file_location=os.getcwd(), show_passage_numbers=True):
    """
    Downloads a specific book of the Bible and saves it as a YAML file
    :param book: Name of the book
    :param file_location: Directory containing the downloaded YAML file. Defaults to the current working directory.
                          The full file path will be <file_location>/NIV/<book>.yaml
    :param show_passage_numbers: If True, passage numbers are provided at the start of each passage's text.
    :return: 0 if the download was successful. Non-zero value if an error occurred.
    """
    # Standardise letter casing with minimal impact to the resulting YAML file
    book = book.title()
    # Check against passing invalid books
    if book not in __chapter_count_mappings.keys():
        print('WARNING: "{0}" is not a valid book'.format(book))
        return 1

    yaml = YAML()
    translation = 'NIV'
    chapters = __chapter_count_mappings[book]
    document = {book: {}}

    # Start from chapter 1 and up to chapter N inclusive
    for chapter in range(1, chapters + 1):
        # Incrementally extract the book contents on a per-chapter basis to avoid exceeding
        # the text limit that can be returned in a single search on the Bible Gateway site.
        passage_list = meaningless.bible_extractor.get_passage_as_list('{0} {1}'.format(book, chapter),
                                                                       show_passage_numbers)
        document[book][chapter] = {}
        passage_num = 1
        for passage in passage_list:
            document[book][chapter][passage_num] = passage
            # TODO In different translations, empty passages are omitted so this is a fairly naive counter
            passage_num += 1

    # Mode can be left as the default value, but don't throw an error when the folder already exists
    os.makedirs('{0}/{1}/'.format(file_location, translation), exist_ok=True)
    # Use UTF-8 encoding to allow for Unicode characters to be written to the file
    with open('{0}/{1}/{2}.yaml'.format(file_location, translation, book), 'w', newline='', encoding='utf-8') as file:
        yaml.dump(document, file)
    file.close()
    return 0

if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    print('Oink')
