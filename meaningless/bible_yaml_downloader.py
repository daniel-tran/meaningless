import os
import multiprocessing
from meaningless.bible_web_extractor import WebExtractor
from meaningless.utilities import yaml_file_interface, common
from meaningless.utilities.exceptions import UnsupportedTranslationError, InvalidPassageError, InvalidSearchError
from ruamel.yaml import YAML


class YAMLDownloader:

    __translations_with_omitted_passages = {
        'ESV': ['Matthew 12:47', 'Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14',
                'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 11:26', 'Mark 15:28',
                'Luke 17:36', 'Luke 23:17',
                'John 5:4',
                'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29',
                'Romans 16:24'],
        'NRSV': ['Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14',
                 'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 11:26', 'Mark 15:28',
                 'Luke 17:36', 'Luke 23:17',
                 'John 5:4',
                 'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29',
                 'Romans 16:24'],
        'NLT': ['Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14',
                'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 11:26', 'Mark 15:28',
                'Luke 17:36', 'Luke 23:17',
                'John 5:4',
                'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29',
                'Romans 16:24'],
        'NASB': ['Matthew 17:21', 'Matthew 18:11', 'Matthew 23:14',
                 'Mark 7:16', 'Mark 9:44', 'Mark 9:46', 'Mark 15:28',
                 'John 5:4',
                 'Acts 8:37', 'Acts 15:34', 'Acts 24:7', 'Acts 28:29',
                 'Romans 16:24']
    }

    def __init__(self, translation='NIV', show_passage_numbers=True, default_directory=os.getcwd(),
                 strip_excess_whitespace=False, enable_multiprocessing=True):
        """
        :param translation: Translation code for the particular passage. For example, 'NIV', 'ESV', 'NLT'
        :param show_passage_numbers: If True, any present passage numbers are preserved.
        :param default_directory: Directory containing the downloaded YAML file.
                                  Defaults to the current working directory.
        :param strip_excess_whitespace: If True, passages don't retain leading & trailing whitespaces as well as
                                        newline characters. Defaults to False.
        :param enable_multiprocessing: If True, downloads are performed using multiple daemon processes, resulting in
                                       lower download times by splitting computations among multiple CPU cores.
                                       Defaults to True.
        """
        self.translation = translation
        self.show_passage_numbers = show_passage_numbers
        self.default_directory = default_directory
        self.strip_excess_whitespace = strip_excess_whitespace
        self.enable_multiprocessing = enable_multiprocessing

    def download_passage(self, book, chapter, passage, file_path=''):
        """
        Downloads a single passage as a YAML file
        :param book: Name of the book
        :param chapter: Chapter number
        :param passage: Passage number
        :param file_path: When specified, saves the YAML file to this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name, and ends in .yaml
        :return: 1 if the download was successful. 0 if an error occurred.
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
        :return: 1 if the download was successful. 0 if an error occurred.
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
        :return: 1 if the download was successful. 0 if an error occurred.
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
        :return: 1 if the download was successful. 0 if an error occurred.
        """
        return self.download_passage_range(book, chapter_from, 1, chapter_to, common.get_end_of_chapter(), file_path)

    def download_book(self, book, file_path=''):
        """
        Downloads a specific book of the Bible and saves it as a YAML file
        :param book: Name of the book
        :param file_path: When specified, saves the YAML file to this location with a custom filename and extension.
                          Using this parameter will take priority over the default_directory class property.
                          Defaults to the default_directory path with the book as the file name, and ends in .yaml
        :return: 1 if the download was successful. 0 if an error occurred.
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
        :return: 1 if the download was successful. 0 if an error occurred.
        """
        translation = self.translation.upper()
        if common.is_unsupported_translation(translation):
            raise UnsupportedTranslationError(translation)
        # Standardise letter casing with minimal impact to the resulting YAML file
        book_name = book.title()

        if common.get_chapter_count(book_name, translation) <= 0:
            raise InvalidPassageError(book_name, chapter_from, passage_from, chapter_to, passage_to, translation)
        # Cap passage components to ensure input validity and minimise web requests by avoiding invalid chapters
        capped_chapter_from = common.get_capped_integer(chapter_from,
                                                        max_value=common.get_chapter_count(book_name, translation))
        capped_passage_from = common.get_capped_integer(passage_from)
        capped_chapter_to = common.get_capped_integer(chapter_to,
                                                      max_value=common.get_chapter_count(book_name, translation))
        capped_passage_to = common.get_capped_integer(passage_to)

        online_bible = WebExtractor(translation=translation, show_passage_numbers=self.show_passage_numbers,
                                    output_as_list=True, passage_separator='',
                                    strip_excess_whitespace_from_list=self.strip_excess_whitespace)

        # Set up the base document with the root-level keys
        # Upon downloading a YAML file, the top-level keys might be ordered differently to when they were inserted.
        # This is likely due to Python not sorting dictionary keys internally, but could be due to something else.
        # This does not affect the information contained in the downloaded YAML file, but could affect file comparisons.
        document = {
            'Info': {
                'Language': common.get_translation_language(translation),
                'Translation': translation
            },
            book_name: {}
        }

        process_pool = multiprocessing.Pool()
        process_results = []

        # Range is extended by 1 to include chapter_to in the loop iteration
        chapter_range = range(capped_chapter_from, capped_chapter_to + 1)
        for chapter in chapter_range:
            passage_initial = 1
            passage_final = common.get_end_of_chapter()
            # Exclude a certain first half of the initial chapter based on where the passage start should be
            if chapter == capped_chapter_from:
                passage_initial = capped_passage_from
            # Exclude a certain last half of the last chapter based on where the passage end should be
            if chapter == capped_chapter_to:
                passage_final = capped_passage_to

            if self.enable_multiprocessing:
                # Asynchronously obtain each set of passages to reduce overall download time.
                # These are daemon processes, so these shouldn't block the program from exiting and should be
                # expected to be garbage collected if the main process is stopped.
                process = process_pool.apply_async(self._get_passages_dict, (online_bible, book_name, chapter,
                                                                             passage_initial, passage_final),
                                                   error_callback=self.__handle_exception_from_process)
                # Add the process result to the list and extract the value later to prioritise doing more work
                process_results.append(process)
            else:
                document[book_name][chapter] = self._get_passages_dict(online_bible, book_name, chapter,
                                                                       passage_initial, passage_final)

        # Close the pool manually, as the garbage collector might not dispose of this automatically
        process_pool.close()
        # Explicitly wait for the processes to finish up in case some processes have heavy workloads
        process_pool.join()

        if self.enable_multiprocessing:
            # When multiprocessing, all process results should be retrieved as a batch operation to minimise
            # the total time cost associated with the "get" method for each result.
            document[book_name] = {chapter: process_results.pop(0).get() for chapter in chapter_range}

        if len(file_path) <= 0:
            file_location = os.path.join(self.default_directory, '{0}.yaml'.format(book_name))
        else:
            file_location = file_path
        return yaml_file_interface.write(file_location, document)

    @staticmethod
    def __handle_exception_from_process(exception):
        """
        A helper function that gets run an exception is received when downloading passages.
        This is not a top-level global function, as it is intended to be solely used within this class.
        :param exception: Exception object that is re-raised after this method completes.
        """
        # Clear the arguments to prevent "stacking" of exception error messages.
        # An empty tuple means the user has to search elsewhere in the stack trace to fine the point of failure.
        exception.args = ()

    def _get_passages_dict(self, online_bible, book, chapter, passage_from, passage_to):
        """
        A helper function that obtains a range of passages and organises them as a dictionary for YAML output.
        Not to be exposed as a usable method, as this function mostly exists so that passage retrieval can be done
        in a multi-processed way. Pre-pending the method name with double underscores causes referencing issues.
        :param online_bible: Instance of WebExtractor to use to download the passages
        :param book: Name of the book
        :param chapter: Chapter number
        :param passage_from: First passage number to get
        :param passage_to: Last passage number to get
        :return: Dictionary of passages, keyed on passage number
        """
        online_bible.output_as_list = True
        passage_list = online_bible.get_passages(book, chapter, passage_from, passage_to)
        # passage_num is the numerical representation of the Unicode passage number at the start of each passage
        passage_num = passage_from
        # self.translation is not used, since getting this far means that the translation used in the
        # earlier call to get_passages is guaranteed to be valid.
        is_translation_with_omitted_passages = online_bible.translation in \
            self.__translations_with_omitted_passages.keys()
        passages = {}
        for passage in passage_list:
            if is_translation_with_omitted_passages:
                # This logic handles translations that omit passages, and have are not considered as valid verse on
                # the Bible Gateway site. It works by checking the passage against the list of known omitted
                # passages for this particular translation, and assigning an empty string if it is omitted.
                # This is to ensure the YAML passage key matches the actual passage contents,
                # regardless of translation.
                passage_string = '{0} {1}:{2}'.format(book, chapter, passage_num)
                if passage_string in self.__translations_with_omitted_passages[online_bible.translation]:
                    passages[passage_num] = ''
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

            passages[passage_num] = passage
            passage_num += 1
        return passages
