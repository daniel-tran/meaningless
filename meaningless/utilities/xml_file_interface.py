import re
import os
import json
import xmltodict
from meaningless.utilities import common

# This is a collection of common methods used for interacting with XML files.


def __get_root_name():
    """
    Gets the top-level tag name used in the document.

    :return: Returns the tag name.
    :rtype: str
    """
    return 'root'


def __get_numeric_prefix():
    """
    Gets the prefix added onto tag names with only numeric characters to make them valid XML tags.

    :return: Returns the tag prefix.
    :rtype: str
    """
    return '_'


def __get_space_placeholder():
    """
    Gets the placeholder character for representing spaces in XML tags.

    :return: Returns the placeholder string
    :rtype: str
    """
    return __get_numeric_prefix()


def write(data_file, document):
    """
    A helper function to write to a XML data file.
    Note that the input data must adhere to the following conventions:
    1. It is a dictionary or similar data structure with key-value pairs.
    2. Key names beyond the first level of the dictionary do not contain spaces.
    3. Any existing keys with underscores are assumed to be placeholders for spaces.

    :param data_file: Path to the data file to write to
    :type data_file: str
    :param document: In-memory data structure, usually a dictionary
    :type document: dict
    :return: Returns 1 on success. Raises an exception when a write problem occurs.
    :rtype: int
    """
    # Only create the directory if it doesn't already exist. This is also to account for directories which are the
    # top level of a given drive (e.g. C:/) which can't be created by the file system due to denied access.
    data_directory = os.path.dirname(data_file)
    if not os.path.exists(data_directory):
        os.makedirs(data_directory, exist_ok=True)
    modified_document = document
    # Replace spaces in tag names, as leaving them in invalidates the document.
    # Note that, for simplicity, this ONLY applies to the first level of tags and is NOT a generic solution.
    for key in modified_document.keys():
        # Always convert the key to a string to ensure that the resulting XML tag name is valid
        new_key = common.cast_to_str_or_int(key, True).replace(' ', __get_space_placeholder())
        modified_document[new_key] = modified_document.pop(key)
    # XML document must only have one root level tag to be a valid structure.
    xml_document = {__get_root_name(): modified_document}
    # Tags cannot start with a number, so prefix them with a placeholder character.
    # Technically, this is not required when writing the document, but not applying the prefix means the
    # XML structure will be rejected by the xmltodict library when trying to read it.
    contents = re.sub(r'<(/?)(\d+)', r'<\1{0}\2'.format(__get_numeric_prefix()),
                      xmltodict.unparse(xml_document, pretty=True, indent='  ')
                      )
    # Use UTF-8 encoding to allow for Unicode characters to be written to the file
    with open(data_file, 'w', newline='', encoding='utf-8') as file:
        file.write(contents)
    return 1


def read(data_file):
    """
    A helper function to read a XML data file.
    Note that the file data must adhere to the following conventions:
    1. The top-level tag is called 'root'.
    2. Tag names at the second level are the only tag names with underscores being used as word separators.
    3. Tag names at the second level with underscores are assumed to be placeholders for spaces.
    4. Tag names that start with a number should only have one underscore as its first character.

    :param data_file: Path to the data file to read
    :type data_file: str
    :return: Contents of the file as an object. Raises an exception when a read problem occurs.
    :rtype: dict
    """
    # Use UTF-8 encoding to be able to read Unicode characters
    with open(data_file, 'r', encoding='utf-8') as file:
        contents = file.read()
    # Extract the inner contents only, since the root element is not needed for reading a XML document
    raw_document = xmltodict.parse(contents)[__get_root_name()]
    # To nicely remove the prefix from keys consisting of only numeric characters, the parsed XML document is
    # dumped as a JSON string, where removing the prefix from the keys still results in a valid document.
    # After removing the prefixes, the document is then reloaded as a JSON document with the correct keys.
    document = json.loads(re.sub(r'"{0}(\d+)'.format(__get_numeric_prefix()), r'"\1', json.dumps(raw_document)))

    # Don't bother processing the document if it only consisted of the generic root level tag
    if document is not None:
        # Revert the space placeholder with an actual space, since the limitations of XML tag naming are removed.
        # Note that, for simplicity, this ONLY applies to the first level of tags and is NOT a generic solution.
        for key in document.keys():
            # Temporarily casting the key to a string just to check if it has a space placeholder
            if __get_space_placeholder() in str(key):
                new_key = key.replace(__get_space_placeholder(), ' ').strip()
            else:
                # Key does not have a space placeholder, so it could be an integer. Try to cast it back, since the
                # limitation of string-only keys is XMl is no longer applicable.
                new_key = common.cast_to_str_or_int(key, False)
            document[new_key] = document.pop(key)
    return document
