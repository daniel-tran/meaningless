import os
from ruamel.yaml import YAML
from ruamel.yaml.parser import ParserError

# This is a collection of common methods used for interacting with YAML files.


def write(data_file, document):
    """
    A helper function to write to a YAML data file. Note that Unix line endings (LF) are used.
    :param data_file: Path to the data file to write to
    :param document: In-memory YAML structure, usually a dictionary
    :return: Returns 1 on success. Raises an exception when a write problem occurs.
    """
    # Mode can be left as the default value, but don't throw an error when the folder already exists
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    # Use UTF-8 encoding to allow for Unicode characters to be written to the file
    with open(data_file, 'w', newline='', encoding='utf-8') as file:
        YAML().dump(document, file)
    return 1


def read(data_file):
    """
    A helper function to read a YAML data file
    :param data_file: Path the data file to read
    :return: Contents of the file as an object. Raises an exception when a read problem occurs.
    """
    # Use UTF-8 encoding to be able to read Unicode characters
    with open(data_file, 'r', encoding='utf-8') as file:
        loader = YAML(typ="safe")  # 'Safe' means it won't load unknown tags
        contents = loader.load(file)
    return contents
