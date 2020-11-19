import os
from ruamel.yaml import YAML
from ruamel.yaml.parser import ParserError

# This is a collection of common methods used for interacting with YAML files.


def write(data_file, document):
    """
    A helper function to write to a YAML data file. Note that Unix line endings (LF) are used.
    :param data_file: Path to the data file to write to
    :param document: In-memory YAML structure
    :return: Returns 0 on success. Returns a non-zero value if an error occurred.
    """
    original_filename_length = len(data_file)
    data_file = os.path.abspath(data_file)
    # This function should only be used for writing YAML output, and NOT for general purpose file writing
    if type(document) is not dict or len(document.keys()) <= 0:
        print('WARNING: Object cannot be formatted as YAML')
        return 1
    if original_filename_length <= 0:
        print('WARNING: Filename is empty')
        return 2
    # Absolute file paths are capped at 260 characters on Windows
    if len(data_file) >= 260:
        print('WARNING: "{0}" exceeds 260 characters. File path length is {1} characters'.format(data_file,
                                                                                                 len(data_file)))
        return 3

    # Mode can be left as the default value, but don't throw an error when the folder already exists
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    # Use UTF-8 encoding to allow for Unicode characters to be written to the file
    with open(data_file, 'w', newline='', encoding='utf-8') as file:
        YAML().dump(document, file)
    file.close()
    return 0


def read(data_file):
    """
    A helper function to read a YAML data file
    :param data_file: Path the data file to read
    :return: Contents of the file as an object. Returns None if the file is empty or a file read error occurred.
    """
    # Easier to proactively detect non-existent YAML file than to rely on reactive exception handling
    # Unlike the write() function, absolute file paths are not required here
    if not os.path.exists(data_file) or len(data_file) <= 0:
        print('WARNING: "{0}" does not exist'.format(data_file))
        return None

    try:
        # Use UTF-8 encoding to be able to read Unicode characters
        with open(data_file, 'r', encoding='utf-8') as file:
            loader = YAML(typ="safe")  # 'Safe' means it won't load unknown tags
            contents = loader.load(file)
        file.close()
    except ParserError:
        # Exception handling requires importing explicit components under ruamel.yaml
        print('WARNING: "{0}" does not contain valid YAML syntax'.format(data_file))
        return None
    return contents
