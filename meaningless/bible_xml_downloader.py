import os
from meaningless.bible_base_downloader import BaseDownloader
from meaningless.utilities import xml_file_interface


class XMLDownloader(BaseDownloader):
    """
    An downloader object that stores Bible passages into a local XML file
    """

    def __init__(self, translation='NIV', show_passage_numbers=True, default_directory=os.getcwd(),
                 strip_excess_whitespace=False, enable_multiprocessing=True, use_ascii_punctuation=False,
                 capitalise_small_caps=False, get_raw_output=False):
        super().__init__(xml_file_interface.write, translation, show_passage_numbers, default_directory,
                         strip_excess_whitespace, enable_multiprocessing, use_ascii_punctuation,
                         file_extension='.xml', write_key_as_string=True, capitalise_small_caps=capitalise_small_caps,
                         get_raw_output=get_raw_output)
