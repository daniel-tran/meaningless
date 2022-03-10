import os
from meaningless.bible_base_extractor import BaseExtractor
from meaningless.utilities import csv_file_interface


class CSVExtractor(BaseExtractor):
    """
    An base extractor object that retrieves Bible passages from a CSV file
    """
    def __init__(self, translation='NIV', show_passage_numbers=True, output_as_list=False,
                 strip_excess_whitespace_from_list=False, default_directory=os.getcwd(),
                 use_ascii_punctuation=False):
        super().__init__(csv_file_interface.read, translation, show_passage_numbers, output_as_list,
                         strip_excess_whitespace_from_list, default_directory, use_ascii_punctuation,
                         file_extension='.csv', read_key_as_string=True)
