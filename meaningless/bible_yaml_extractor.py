import os
from meaningless.bible_base_extractor import BaseExtractor
from meaningless.utilities import yaml_file_interface


class YAMLExtractor(BaseExtractor):
    """
    An base extractor object that retrieves Bible passages from a YAML file
    """
    def __init__(self, translation='NIV', show_passage_numbers=True, output_as_list=False,
                 strip_excess_whitespace_from_list=False, default_directory=os.getcwd(),
                 use_ascii_punctuation=False, add_minimal_copyright=False):
        super().__init__(yaml_file_interface.read, translation, show_passage_numbers, output_as_list,
                         strip_excess_whitespace_from_list, default_directory, use_ascii_punctuation,
                         add_minimal_copyright, file_extension='.yaml', read_key_as_string=False)
