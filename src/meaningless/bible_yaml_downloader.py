import os
from meaningless import bible_extractor
from meaningless.utilities import yaml_file_interface, common
from ruamel.yaml import YAML

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


def yaml_download_book(book, file_location=os.getcwd(), show_passage_numbers=True, translation='NIV',
                       strip_excess_whitespace=False):
    """
    Downloads a specific book of the Bible and saves it as a YAML file
    :param book: Name of the book
    :param file_location: Directory containing the downloaded YAML file. Defaults to the current working directory.
                          The full file path will be <file_location>/<translation>/<book>.yaml
    :param show_passage_numbers: If True, passage numbers are provided at the start of each passage's text.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_excess_whitespace: If True, passages don't retain leading & trailing whitespaces + newline characters.
    :return: 0 if the download was successful. Non-zero value if an error occurred.
    """
    # Check against passing invalid books
    if common.get_chapter_count(book, translation) <= 0:
        print('WARNING: "{0}" is not a valid book, or "{1}" is an unsupported translation'.format(book, translation))
        return 1
    return yaml_download_passage_range(book, 1, 1, common.get_chapter_count(book, translation),
                                       common.get_end_of_chapter(), file_location, show_passage_numbers,
                                       translation, strip_excess_whitespace)


def yaml_download_passage(book, chapter, passage, file_location=os.getcwd(), show_passage_numbers=True,
                          translation='NIV', strip_excess_whitespace=False):
    """

    Downloads a single passage as a YAML file
    :param book: Name of the book
    :param chapter: Chapter number
    :param passage: Passage number
    :param file_location: Directory containing the downloaded YAML file. Defaults to the current working directory.
                          The full file path will be <file_location>/<translation>/<book>.yaml
    :param show_passage_numbers: If True, passage numbers are provided at the start of each passage's text.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_excess_whitespace: If True, passages don't retain leading & trailing whitespaces + newline characters.
    :return: 0 if the download was successful. Non-zero value if an error occurred.
    """
    return yaml_download_passage_range(book, chapter, passage, chapter, passage, file_location, show_passage_numbers,
                                       translation, strip_excess_whitespace)


def yaml_download_passages(book, chapter, passage_from, passage_to, file_location=os.getcwd(),
                           show_passage_numbers=True, translation='NIV', strip_excess_whitespace=False):
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
    :param strip_excess_whitespace: If True, passages don't retain leading & trailing whitespaces + newline characters.
    :return: 0 if the download was successful. Non-zero value if an error occurred.
    """
    return yaml_download_passage_range(book, chapter, passage_from, chapter, passage_to, file_location,
                                       show_passage_numbers, translation, strip_excess_whitespace)


def yaml_download_chapter(book, chapter, file_location=os.getcwd(), show_passage_numbers=True, translation='NIV',
                          strip_excess_whitespace=False):
    """
    Downloads a single chapter as a YAML file
    :param book: Name of the book
    :param chapter: Chapter number
    :param file_location: Directory containing the downloaded YAML file. Defaults to the current working directory.
                          The full file path will be <file_location>/<translation>/<book>.yaml
    :param show_passage_numbers: If True, passage numbers are provided at the start of each passage's text.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_excess_whitespace: If True, passages don't retain leading & trailing whitespaces + newline characters.
    :return: 0 if the download was successful. Non-zero value if an error occurred.
    """
    return yaml_download_passage_range(book, chapter, 1, chapter, common.get_end_of_chapter(),
                                       file_location, show_passage_numbers, translation, strip_excess_whitespace)


def yaml_download_chapters(book, chapter_from, chapter_to, file_location=os.getcwd(), show_passage_numbers=True,
                           translation='NIV', strip_excess_whitespace=False):
    """
    Downloads a range of passages from a specified chapter selection as a YAML file
    :param book: Name of the book
    :param chapter_from: First chapter number to get
    :param chapter_to: Last chapter number to get
    :param file_location: Directory containing the downloaded YAML file. Defaults to the current working directory.
                          The full file path will be <file_location>/<translation>/<book>.yaml
    :param show_passage_numbers: If True, passage numbers are provided at the start of each passage's text.
    :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
    :param strip_excess_whitespace: If True, passages don't retain leading & trailing whitespaces + newline characters.
    :return: 0 if the download was successful. Non-zero value if an error occurred.
    """
    return yaml_download_passage_range(book, chapter_from, 1, chapter_to, common.get_end_of_chapter(),
                                       file_location, show_passage_numbers, translation, strip_excess_whitespace)


def yaml_download_passage_range(book, chapter_from, passage_from, chapter_to, passage_to, file_location=os.getcwd(),
                                show_passage_numbers=True, translation='NIV', strip_excess_whitespace=False):
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
    :param strip_excess_whitespace: If True, passages don't retain leading & trailing whitespaces + newline characters.
    :return: 0 if the download was successful. Non-zero value if an error occurred.
    """
    # Standardise letter casing with minimal impact to the resulting YAML file
    book = book.title()

    if common.get_chapter_count(book, translation) <= 0:
        print('WARNING: "{0}" is not a valid book, or "{1}" is an unsupported translation'.format(book, translation))
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

        passage_list = bible_extractor.get_online_passages(book, chapter, passage_initial, passage_final, '',
                                                           show_passage_numbers, translation, True,
                                                           strip_excess_whitespace)
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

            # First passage of the chapter may not always have a verse number.
            # Unclear if this is a formatting issue on the Bible Gateway site, but it is added for consistency.
            # This is not done on the web extractor due to the difficulty of selecting the first passage in an
            # arbitrary range.
            if passage_num == 1 and show_passage_numbers and not passage.startswith('\u00b9 '):
                passage = '\u00b9 {0}'.format(passage)

            document[book][chapter][passage_num] = passage
            passage_num += 1

    return yaml_file_interface.write('{0}/{1}/{2}.yaml'.format(file_location, translation, book), document)

if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    print('Oink')
