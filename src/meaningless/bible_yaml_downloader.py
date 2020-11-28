import os
from meaningless.bible_extractor import WebExtractor
from meaningless.utilities import yaml_file_interface, common
from ruamel.yaml import YAML


class YAMLDownloader:

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

    def __init__(self, translation='NIV', show_passage_numbers=True, file_location=os.getcwd(),
                 strip_excess_whitespace=False, include_misc_info=False):
        """
        :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
        :param show_passage_numbers: If True, any present passage numbers are preserved.
        :param file_location: Directory containing the downloaded YAML file. Defaults to the current working directory.
        :param strip_excess_whitespace: If True, passages don't retain leading & trailing whitespaces as well as
                                        newline characters.
        :param include_misc_info: If True, additional information is included in the YAML file, such as the translation.
        """
        self.translation = translation
        self.show_passage_numbers = show_passage_numbers
        self.file_location = file_location
        self.strip_excess_whitespace = strip_excess_whitespace
        self.include_misc_info = include_misc_info

    def download_passage(self, book, chapter, passage):
        """
        Downloads a single passage as a YAML file
        :param book: Name of the book
        :param chapter: Chapter number
        :param passage: Passage number
        :return: 0 if the download was successful. Non-zero value if an error occurred.
        """
        return self.download_passage_range(book, chapter, passage, chapter, passage)

    def download_passages(self, book, chapter, passage_from, passage_to):
        """
        Downloads a range of passages of the same chapter as a YAML file
        :param book: Name of the book
        :param chapter: Chapter number
        :param passage_from: First passage number to get
        :param passage_to: Last passage number to get
        :return: 0 if the download was successful. Non-zero value if an error occurred.
        """
        return self.download_passage_range(book, chapter, passage_from, chapter, passage_to)

    def download_chapter(self, book, chapter):
        """
        Downloads a single chapter as a YAML file
        :param book: Name of the book
        :param chapter: Chapter number
        :return: 0 if the download was successful. Non-zero value if an error occurred.
        """
        return self.download_passage_range(book, chapter, 1, chapter, common.get_end_of_chapter())

    def download_chapters(self, book, chapter_from, chapter_to):
        """
        Downloads a range of passages from a specified chapter selection as a YAML file
        :param book: Name of the book
        :param chapter_from: First chapter number to get
        :param chapter_to: Last chapter number to get
        :return: 0 if the download was successful. Non-zero value if an error occurred.
        """
        return self.download_passage_range(book, chapter_from, 1, chapter_to, common.get_end_of_chapter())

    def download_book(self, book):
        """
        Downloads a specific book of the Bible and saves it as a YAML file
        :param book: Name of the book
        :return: 0 if the download was successful. Non-zero value if an error occurred.
        """
        return self.download_passage_range(book, 1, 1, common.get_chapter_count(book, self.translation),
                                           common.get_end_of_chapter())

    def download_passage_range(self, book, chapter_from, passage_from, chapter_to, passage_to):
        """
        Downloads a range of passages from one specific passage to another passage as a YAML file
        :param book: Name of the book
        :param chapter_from: First chapter number to get
        :param passage_from: First passage number to get in the first chapter
        :param chapter_to: Last chapter number to get
        :param passage_to: Last passage number to get in the last chapter
        """
        # Standardise letter casing with minimal impact to the resulting YAML file
        book = book.title()

        if common.get_chapter_count(book, self.translation) <= 0:
            print('WARNING: "{0}" is not a valid book, or "{1}" is an unsupported translation'.format(book,
                                                                                                      self.translation))
            return 1

        is_translation_with_omitted_passages = self.translation in self.__translations_with_omitted_passages.keys()
        online_bible = WebExtractor(translation=self.translation, show_passage_numbers=self.show_passage_numbers,
                                    output_as_list=True, passage_separator='',
                                    strip_excess_whitespace_from_list=self.strip_excess_whitespace)

        # Set up the base document with the root-level keys
        # While the order of insertion matters, there are some books such as Philemon where the misc. info is placed
        # after the passage contents even though the logic adds the misc. info first. The cause is currently unknown.
        document = {}
        if self.include_misc_info:
            document['Info'] = {
                'Language': common.get_translation_language(self.translation),
                'Translation': self.translation
            }
        document[book] = {}

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

            passage_list = online_bible.get_passages(book, chapter, passage_initial, passage_final)
            document[book][chapter] = {}

            for passage in passage_list:
                if is_translation_with_omitted_passages:
                    # This logic handles translations that omit passages, and have are not considered as valid verse on
                    # the Bible Gateway site. It works by checking the passage against the list of known omitted
                    # passages for this particular translation, and assigning an empty string if it is omitted.
                    # This is to ensure the YAML passage key matches the actual passage contents,
                    # regardless of translation.
                    passage_string = '{0} {1}:{2}'.format(book, chapter, passage_num)
                    if passage_string in self.__translations_with_omitted_passages[self.translation]:
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
                if passage_num == 1 and self.show_passage_numbers and not passage.startswith('\u00b9 '):
                    passage = '\u00b9 {0}'.format(passage)

                document[book][chapter][passage_num] = passage
                passage_num += 1

        return yaml_file_interface.write('{0}/{1}/{2}.yaml'.format(self.file_location, self.translation, book),
                                         document)

if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    print('Oink')
