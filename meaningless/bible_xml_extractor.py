import os
from meaningless.bible_base_extractor import BaseExtractor
from meaningless.utilities import xml_file_interface, legacy_xml_file_interface


class XMLExtractor(BaseExtractor):
    """
    An base extractor object that retrieves Bible passages from an XML file

    To process files using the legacy XML structure prior to version 0.7.0, set `use_legacy_mode=True`.
    Note that using this setting is considered deprecated behaviour, and will likely be removed in a future version.
    """
    def __init__(self, translation='NIV', show_passage_numbers=True, output_as_list=False,
                 strip_excess_whitespace_from_list=False, default_directory=os.getcwd(),
                 use_ascii_punctuation=False, use_legacy_mode=False):
        function = xml_file_interface.read if not use_legacy_mode else legacy_xml_file_interface.read
        super().__init__(function, translation, show_passage_numbers, output_as_list,
                         strip_excess_whitespace_from_list, default_directory, use_ascii_punctuation,
                         file_extension='.xml', read_key_as_string=True)
