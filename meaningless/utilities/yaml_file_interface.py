import os
from ruamel.yaml import YAML

# This is a collection of common methods used for interacting with YAML files.


def write(data_file, document):
    """
    A helper function to write to a YAML data file. Note that Unix line endings (LF) are used.

    :param data_file: Path to the data file to write to
    :type data_file: str
    :param document: In-memory YAML structure, usually a dictionary
    :type document: dict
    :return: Returns 1 on success. Raises an exception when a write problem occurs.
    :rtype: int
    """
    max_line_length = 2048
    # Only create the directory if it doesn't already exist. This is also to account for directories which are the
    # top level of a given drive (e.g. C:/) which can't be created by the file system due to denied access.
    data_directory = os.path.dirname(data_file)
    if not os.path.exists(data_directory):
        os.makedirs(data_directory, exist_ok=True)
    # Use UTF-8 encoding to allow for Unicode characters to be written to the file
    with open(data_file, 'w', newline='', encoding='utf-8') as file:
        loader = YAML()
        # For multiline strings, YAML files assume a single space between words that connect multiple lines, which can
        # be problematic when a line ends with a newline character. Simply extending the line width fixes this.
        loader.width = max_line_length
        loader.dump(document, file)
    return 1


def read(data_file):
    """
    A helper function to read a YAML data file

    :param data_file: Path the data file to read
    :type data_file: str
    :return: Contents of the file as an object. Raises an exception when a read problem occurs.
    :rtype: dict
    """
    # Use UTF-8 encoding to be able to read Unicode characters
    with open(data_file, 'r', encoding='utf-8') as file:
        loader = YAML(typ="safe")  # 'Safe' means it won't load unknown tags
        contents = loader.load(file)
    return contents
