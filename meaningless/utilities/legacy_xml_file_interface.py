import re
import os
import json
import xmltodict
from meaningless.utilities import common

# This is a collection of common methods used for interacting with XML files with the legacy file structure.


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


def __get_cdata_key():
    """
    Gets the placeholder string for the cdata key that is automatically added into a parsed XML document

    :return: Returns the key name
    :rtype: str
    """
    return ''


def __remove_xml_placeholders_from_key(path, key, value):
    """
    A post-processing function when parsing the XML document to normalise keys into a more familiar format.

    :param path: Path from the document root to the key-value pair. Required as part of the xmltodict interface.
    :type path: str
    :param key: Dictionary key in the document. Required as part of the xmltodict interface.
    :type key: str
    :param value: Dictionary value in the document. Required as part of the xmltodict interface.
    :type value: str
    :return: Returns the modified key-value pair
    :rtype: tuple
    """
    # Revert the space placeholder with an actual space, since the limitations of XML tag naming are removed.
    # Since the space placeholder is a reserved string, any legitimate use for this in a tag name is ignored.
    # Strip excess whitespace afterwards to remove converted space placeholders at the start or end of a string.
    new_key = key.replace(__get_space_placeholder(), ' ').replace(__get_numeric_prefix(), '').strip()
    # Omit keys that are empty or consisted only of space placeholders, which would have reduced to an empty string.
    # This is also a convenient way to remove the generated cdata key, by setting it to something that can be ignored.
    if len(new_key) <= 0:
        return
    # Reading a tag without contents resolve to None, which is incorrect in the case of omitted passages
    new_value = value if value is not None else ''
    return new_key, new_value


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

    .. deprecated:: 0.7.0
       Use xml_file_interface instead for XML file interactions
    """
    # Only create the directory if it doesn't already exist. This is also to account for directories which are the
    # top level of a given drive (e.g. C:/) which can't be created by the file system due to denied access.
    data_directory = os.path.dirname(data_file)
    if not os.path.exists(data_directory):
        os.makedirs(data_directory, exist_ok=True)
    modified_document = document
    # Replace spaces in tag names, as leaving them in invalidates the document.
    # Note that, for simplicity, this ONLY applies to the first level of tags and is NOT a generic solution.
    for key in list(modified_document.keys()):
        # Always convert the key to a string to ensure that the resulting XML tag name is valid
        new_key = common.cast_to_str_or_int(key, True).replace(' ', __get_space_placeholder())
        modified_document[new_key] = modified_document.pop(key)
    # XML document must only have one root level tag to be a valid structure.
    modified_document = {__get_root_name(): modified_document}
    # Ensure all keys in the data structure are strings, since the xmltodict library will assume this when processing
    # the document. Use conversion to JSON to achieve this, since it automatically casts numeric keys as strings.
    modified_document = json.loads(json.dumps(modified_document))
    # Tags cannot start with a number, so prefix them with a placeholder character.
    # Technically, this is not required when writing the document, but not applying the prefix means the
    # XML structure will be rejected by the xmltodict library when trying to read it.
    contents = re.sub(r'<(/?)(\d+)', r'<\1{0}\2'.format(__get_numeric_prefix()),
                      xmltodict.unparse(modified_document, pretty=True, indent='  ')
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
    2. Tag names with underscores are assumed to be placeholders for spaces.
    3. Tag names that start with a number should only be prefixed with underscores.

    :param data_file: Path to the data file to read
    :type data_file: str
    :return: Contents of the file as an object. Raises an exception when a read problem occurs.
    :rtype: dict

    .. deprecated:: 0.7.0
       Use xml_file_interface instead for XML file interactions
    """
    # Use UTF-8 encoding to be able to read Unicode characters
    with open(data_file, 'r', encoding='utf-8') as file:
        contents = file.read()
    # Since white space and newlines are preserved, the side effect is that a cdata key is automatically added into
    # each level of the document, with its value being spaces and newline characters.
    raw_document = xmltodict.parse(contents, strip_whitespace=False, cdata_key=__get_cdata_key(),
                                   postprocessor=__remove_xml_placeholders_from_key)
    return raw_document[__get_root_name()]
