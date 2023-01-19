import os
from meaningless.bible_base_downloader import BaseDownloader
from meaningless.utilities import xml_file_interface, legacy_xml_file_interface


class XMLDownloader(BaseDownloader):
    """
    An downloader object that stores Bible passages into a local XML file

    To download files using the legacy XML structure prior to version 0.7.0, set `use_legacy_mode=True`.
    Note that using this setting is considered deprecated behaviour, and will likely be removed in a future version.
    """

    def __init__(self, translation='NIV', show_passage_numbers=True, default_directory=os.getcwd(),
                 strip_excess_whitespace=False, enable_multiprocessing=True, use_ascii_punctuation=False,
                 use_legacy_mode=False):
        function = xml_file_interface.write if not use_legacy_mode else legacy_xml_file_interface.write
        super().__init__(function, translation, show_passage_numbers, default_directory,
                         strip_excess_whitespace, enable_multiprocessing, use_ascii_punctuation,
                         file_extension='.xml', write_key_as_string=True)
