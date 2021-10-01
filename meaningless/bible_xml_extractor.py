import os
from meaningless.bible_base_extractor import BaseExtractor
from meaningless.utilities import xml_file_interface


class XMLExtractor(BaseExtractor):
    """
    An base extractor object that retrieves Bible passages from an XML file
    """
    def __init__(self, translation='NIV', show_passage_numbers=True, output_as_list=False,
                 strip_excess_whitespace_from_list=False, default_directory=os.getcwd(),
                 use_ascii_punctuation=False):
        super().__init__(xml_file_interface.read, translation, show_passage_numbers, output_as_list,
                         strip_excess_whitespace_from_list, default_directory, use_ascii_punctuation,
                         file_extension='.xml', read_key_as_string=True)
