import os
from meaningless import bible_list_extractor
from meaningless.utilities import yaml_file_interface, common
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

# A list of translations that have known omitted passages.
# Translations missing from this list are either not supported, or handle omitted passages in some way.
__translations_with_omitted_passages = {
    'ESV': ['Matthew 12:47', 'Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14',
            'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 15:28', 'Luke 17:36', 'Luke 23:17', 'John 5:4',
            'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29', 'Romans 16:24'],
    'NRSV': ['Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14', 'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 11:26',
             'Mark 15:28', 'Luke 17:36', 'Luke 23:17', 'John 5:4', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29',
             'Romans 16:24'],
    'NLT': ['Matthew 18:11', 'Matthew 23:14', 'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 11:26', 'Mark 15:28',
            'Luke 17:36', 'Luke 23:17', 'John 5:4', 'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29',
            'Romans 16:24'],
    'NASB': ['Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14', 'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 15:28',
             'John 5:4', 'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29', 'Romans 16:24']
}


def yaml_download(book, file_location=os.getcwd(), show_passage_numbers=True, translation='NIV',
                  strip_whitespaces=False):
    """
    Downloads a specific book of the Bible and saves it as a YAML file
    :param book: Name of the book
    :param file_location: Directory containing the downloaded YAML file. Defaults to the current working directory.
                          The full file path will be <file_location>/<translation>/<book>.yaml
    :param show_passage_numbers: If True, passage numbers are provided at the start of each passage's text.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_whitespaces: If True, passages do not retain leading and trailing whitespaces and newline characters.
    :return: 0 if the download was successful. Non-zero value if an error occurred.
    """
    # Check against passing invalid books
    if book.title() not in __chapter_count_mappings.keys():
        print('WARNING: "{0}" is not a valid book'.format(book))
        return 1
    return yaml_download_passage_range(book, 1, 1, __chapter_count_mappings[book], common.get_end_of_chapter(),
                                       file_location, show_passage_numbers, translation, strip_whitespaces)


def yaml_download_passage(book, chapter, passage, file_location=os.getcwd(), show_passage_numbers=True,
                          translation='NIV', strip_whitespaces=False):
    """

    Downloads a single passage as a YAML file
    :param book: Name of the book
    :param chapter: Chapter number
    :param passage: Passage number
    :param file_location: Directory containing the downloaded YAML file. Defaults to the current working directory.
                          The full file path will be <file_location>/<translation>/<book>.yaml
    :param show_passage_numbers: If True, passage numbers are provided at the start of each passage's text.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_whitespaces: If True, passages do not retain leading and trailing whitespaces and newline characters.
    :return: 0 if the download was successful. Non-zero value if an error occurred.
    """
    return yaml_download_passage_range(book, chapter, passage, chapter, passage, file_location, show_passage_numbers,
                                       translation, strip_whitespaces)


def yaml_download_passages(book, chapter, passage_from, passage_to, file_location=os.getcwd(),
                           show_passage_numbers=True, translation='NIV', strip_whitespaces=False):
    """
    Downloads a range of passages of the same chapter as a YAML file
    :param book: Name of the book
    :param chapter: Chapter number
    :param passage_from: First passage number to get
    :param passage_to: Last passage number to get
    :param file_location: Directory containing the downloaded YAML file. Defaults to the current working directory.
                          The full file path will be <file_location>/<translation>/<book>.yaml
    :param show_passage_numbers: If True, passage numbers are provided at the start of each passage's text.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_whitespaces: If True, passages do not retain leading and trailing whitespaces and newline characters.
    :return: 0 if the download was successful. Non-zero value if an error occurred.
    """
    return yaml_download_passage_range(book, chapter, passage_from, chapter, passage_to, file_location,
                                       show_passage_numbers, translation, strip_whitespaces)


def yaml_download_chapter(book, chapter, file_location=os.getcwd(), show_passage_numbers=True, translation='NIV',
                          strip_whitespaces=False):
    """
    Downloads a single chapter as a YAML file
    :param book: Name of the book
    :param chapter: Chapter number
    :param file_location: Directory containing the downloaded YAML file. Defaults to the current working directory.
                          The full file path will be <file_location>/<translation>/<book>.yaml
    :param show_passage_numbers: If True, passage numbers are provided at the start of each passage's text.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_whitespaces: If True, passages do not retain leading and trailing whitespaces and newline characters.
    :return: 0 if the download was successful. Non-zero value if an error occurred.
    """
    return yaml_download_passage_range(book, chapter, 1, chapter, common.get_end_of_chapter(),
                                       file_location, show_passage_numbers, translation, strip_whitespaces)


def yaml_download_chapters(book, chapter_from, chapter_to, file_location=os.getcwd(), show_passage_numbers=True,
                           translation='NIV', strip_whitespaces=False):
    """
    Downloads a range of passages from a specified chapter selection as a YAML file
    :param book: Name of the book
    :param chapter_from: First chapter number to get
    :param chapter_to: Last chapter number to get
    :param file_location: Directory containing the downloaded YAML file. Defaults to the current working directory.
                          The full file path will be <file_location>/<translation>/<book>.yaml
    :param show_passage_numbers: If True, passage numbers are provided at the start of each passage's text.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_whitespaces: If True, passages do not retain leading and trailing whitespaces and newline characters.
    :return: 0 if the download was successful. Non-zero value if an error occurred.
    """
    return yaml_download_passage_range(book, chapter_from, 1, chapter_to, common.get_end_of_chapter(),
                                       file_location, show_passage_numbers, translation, strip_whitespaces)


def yaml_download_passage_range(book, chapter_from, passage_from, chapter_to, passage_to, file_location=os.getcwd(),
                                show_passage_numbers=True, translation='NIV', strip_whitespaces=False):
    """
    Downloads a range of passages from one specific passage to another passage as a YAML file
    :param book: Name of the book
    :param chapter_from: First chapter number to get
    :param passage_from: First passage number to get in the first chapter
    :param chapter_to: Last chapter number to get
    :param passage_to: Last passage number to get in the last chapter
    :param file_location: Directory containing the downloaded YAML file. Defaults to the current working directory.
                          The full file path will be <file_location>/<translation>/<book>.yaml
    :param show_passage_numbers: If True, passage numbers are provided at the start of each passage's text.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_whitespaces: If True, passages do not retain leading and trailing whitespaces and newline characters.
    :return: 0 if the download was successful. Non-zero value if an error occurred.
    """
    # Standardise letter casing with minimal impact to the resulting YAML file
    book = book.title()
    # Check against passing invalid books
    if book not in __chapter_count_mappings.keys():
        print('WARNING: "{0}" is not a valid book'.format(book))
        return 1

    is_translation_with_omitted_passages = translation in __translations_with_omitted_passages.keys()
    document = {book: {}}

    # Range is extended by 1 to include chapter_to in the loop iteration
    for chapter in range(chapter_from, chapter_to + 1):
        passage_initial = 1
        passage_final = common.get_end_of_chapter()
        passage_num = 1
        # Exclude a certain first half of the initial chapter based on where the passage start should be
        if chapter == chapter_from:
            passage_initial = passage_from
            passage_num = passage_from
        # Exclude a certain last half of the last chapter based on where the passage end should be
        if chapter == chapter_to:
            passage_final = passage_to

        passage_list = bible_list_extractor.get_passages(book, chapter, passage_initial, passage_final,
                                                         show_passage_numbers, translation, strip_whitespaces)
        document[book][chapter] = {}

        for passage in passage_list:
            if is_translation_with_omitted_passages:
                # This logic handles translations that omit passages, and have are not considered as valid verse on
                # the Bible Gateway site. It works by checking the passage against the list of known omitted
                # passages for this particular translation, and assigning an empty string if it is omitted.
                # This is to ensure the YAML passage key matches the actual passage contents, regardless of translation.
                passage_string = '{0} {1}:{2}'.format(book, chapter, passage_num)
                if passage_string in __translations_with_omitted_passages[translation]:
                    document[book][chapter][passage_num] = ''
                    # Since this passage isn't supposed to exist in the given translation but it is still registered
                    # in the YAML file, the number is upped twice in this loop iteration - once for the omitted
                    # passage and once for the passage after the omitted passage (whose contents is accessible in
                    # this particular iteration)
                    passage_num += 1

            document[book][chapter][passage_num] = passage
            passage_num += 1

    return yaml_file_interface.write('{0}/{1}/{2}.yaml'.format(file_location, translation, book), document)

if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    print('Oink')
