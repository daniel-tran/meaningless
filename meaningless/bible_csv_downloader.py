import os
from meaningless.bible_base_downloader import BaseDownloader
from meaningless.utilities import csv_file_interface


class CSVDownloader(BaseDownloader):
    """
    An downloader object that stores Bible passages into a local CSV file
    """

    def __init__(self, translation='NIV', show_passage_numbers=True, default_directory=os.getcwd(),
                 strip_excess_whitespace=False, enable_multiprocessing=True, use_ascii_punctuation=False):
        super().__init__(csv_file_interface.write, translation, show_passage_numbers, default_directory,
                         strip_excess_whitespace, enable_multiprocessing, use_ascii_punctuation,
                         file_extension='.csv', write_key_as_string=False)
