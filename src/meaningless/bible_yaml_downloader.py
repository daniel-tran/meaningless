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

    def __init__(self, translation='NIV', show_passage_numbers=True, default_directory=os.getcwd(),
                 strip_excess_whitespace=False, include_misc_info=False):
        """
        :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
        :param show_passage_numbers: If True, any present passage numbers are preserved.
        :param default_directory: Directory containing the downloaded YAML file.
                                  Defaults to the current working directory.
        :param strip_excess_whitespace: If True, passages don't retain leading & trailing whitespaces as well as
                                        newline characters.
        :param include_misc_info: If True, additional information is included in the YAML file, such as the translation.
        """
        self.translation = translation
        self.show_passage_numbers = show_passage_numbers
        self.default_directory = default_directory
        self.strip_excess_whitespace = strip_excess_whitespace
        self.include_misc_info = include_misc_info

    def download_passage(self, book, chapter, passage, file_path=''):
        """
        Downloads a single passage as a YAML file
        :param book: Name of the book
        :param chapter: Chapter number
        :param passage: Passage number
        :param file_path: When specified, saves the YAML file to this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name, and ends in .yaml
        :return: 0 if the download was successful. Non-zero value if an error occurred.
        """
        return self.download_passage_range(book, chapter, passage, chapter, passage, file_path)

    def download_passages(self, book, chapter, passage_from, passage_to, file_path=''):
        """
        Downloads a range of passages of the same chapter as a YAML file
        :param book: Name of the book
        :param chapter: Chapter number
        :param passage_from: First passage number to get
        :param passage_to: Last passage number to get
        :param file_path: When specified, saves the YAML file to this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name, and ends in .yaml
        :return: 0 if the download was successful. Non-zero value if an error occurred.
        """
        return self.download_passage_range(book, chapter, passage_from, chapter, passage_to, file_path)

    def download_chapter(self, book, chapter, file_path=''):
        """
        Downloads a single chapter as a YAML file
        :param book: Name of the book
        :param chapter: Chapter number
        :param file_path: When specified, saves the YAML file to this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name, and ends in .yaml
        :return: 0 if the download was successful. Non-zero value if an error occurred.
        """
        return self.download_passage_range(book, chapter, 1, chapter, common.get_end_of_chapter(), file_path)

    def download_chapters(self, book, chapter_from, chapter_to, file_path=''):
        """
        Downloads a range of passages from a specified chapter selection as a YAML file
        :param book: Name of the book
        :param chapter_from: First chapter number to get
        :param chapter_to: Last chapter number to get
        :param file_path: When specified, saves the YAML file to this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name, and ends in .yaml
        :return: 0 if the download was successful. Non-zero value if an error occurred.
        """
        return self.download_passage_range(book, chapter_from, 1, chapter_to, common.get_end_of_chapter(), file_path)

    def download_book(self, book, file_path=''):
        """
        Downloads a specific book of the Bible and saves it as a YAML file
        :param book: Name of the book
        :param file_path: When specified, saves the YAML file to this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name, and ends in .yaml
        :return: 0 if the download was successful. Non-zero value if an error occurred.
        """
        return self.download_passage_range(book, 1, 1, common.get_chapter_count(book, self.translation),
                                           common.get_end_of_chapter(), file_path)

    def download_passage_range(self, book, chapter_from, passage_from, chapter_to, passage_to, file_path=''):
        """
        Downloads a range of passages from one specific passage to another passage as a YAML file
        :param book: Name of the book
        :param chapter_from: First chapter number to get
        :param passage_from: First passage number to get in the first chapter
        :param chapter_to: Last chapter number to get
        :param passage_to: Last passage number to get in the last chapter
        :param file_path: When specified, saves the YAML file to this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name, and ends in .yaml
        :return: 0 if the download was successful. Non-zero value if an error occurred.
        """
        # Standardise letter casing with minimal impact to the resulting YAML file
        book_name = book.title()

        if common.get_chapter_count(book_name, self.translation) <= 0:
            print('WARNING: "{0}" is not a valid book, or "{1}" is an unsupported translation'.format(book_name,
                                                                                                      self.translation))
            return 1
        # Cap passage components to ensure input validity and minimise web requests by avoiding invalid chapters
        capped_chapter_from = common.get_capped_integer(chapter_from,
                                                        max_value=common.get_chapter_count(book_name, self.translation))
        capped_passage_from = common.get_capped_integer(passage_from)
        capped_chapter_to = common.get_capped_integer(chapter_to,
                                                      max_value=common.get_chapter_count(book_name, self.translation))
        capped_passage_to = common.get_capped_integer(passage_to)

        is_translation_with_omitted_passages = self.translation in self.__translations_with_omitted_passages.keys()
        online_bible = WebExtractor(translation=self.translation, show_passage_numbers=self.show_passage_numbers,
                                    output_as_list=True, passage_separator='',
                                    strip_excess_whitespace_from_list=self.strip_excess_whitespace)

        # Set up the base document with the root-level keys
        # Upon downloading a YAML file, the top-level keys might be ordered differently to when they were inserted.
        # This is likely due to Python not sorting dictionary keys internally, but could be due to something else.
        # This does not affect the information contained in the downloaded YAML file, but could affect file comparisons.
        document = {}
        if self.include_misc_info:
            document['Info'] = {
                'Language': common.get_translation_language(self.translation),
                'Translation': self.translation
            }
        document[book_name] = {}

        # Range is extended by 1 to include chapter_to in the loop iteration
        for chapter in range(capped_chapter_from, capped_chapter_to + 1):
            passage_initial = 1
            passage_final = common.get_end_of_chapter()
            passage_num = 1
            # Exclude a certain first half of the initial chapter based on where the passage start should be
            if chapter == capped_chapter_from:
                passage_initial = capped_passage_from
                passage_num = capped_passage_from
            # Exclude a certain last half of the last chapter based on where the passage end should be
            if chapter == capped_chapter_to:
                passage_final = capped_passage_to

            passage_list = online_bible.get_passages(book_name, chapter, passage_initial, passage_final)
            document[book_name][chapter] = {}

            for passage in passage_list:
                if is_translation_with_omitted_passages:
                    # This logic handles translations that omit passages, and have are not considered as valid verse on
                    # the Bible Gateway site. It works by checking the passage against the list of known omitted
                    # passages for this particular translation, and assigning an empty string if it is omitted.
                    # This is to ensure the YAML passage key matches the actual passage contents,
                    # regardless of translation.
                    passage_string = '{0} {1}:{2}'.format(book_name, chapter, passage_num)
                    if passage_string in self.__translations_with_omitted_passages[self.translation]:
                        document[book_name][chapter][passage_num] = ''
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

                document[book_name][chapter][passage_num] = passage
                passage_num += 1

        if len(file_path) <= 0:
            file_location = os.path.join(self.default_directory, '{0}.yaml'.format(book_name))
        else:
            file_location = file_path
        return yaml_file_interface.write(file_location, document)

if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    print('Oink')
