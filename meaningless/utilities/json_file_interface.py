import os
import json

# This is a collection of common methods used for interacting with JSON files.


def write(data_file, document):
    """
    A helper function to write to a JSON data file.

    :param data_file: Path to the data file to write to
    :type data_file: str
    :param document: In-memory JSON structure, usually a dictionary
    :type document: dict
    :return: Returns 1 on success. Raises an exception when a write problem occurs.
    :rtype: int
    """
    # Only create the directory if it doesn't already exist. This is also to account for directories which are the
    # top level of a given drive (e.g. C:/) which can't be created by the file system due to denied access.
    data_directory = os.path.dirname(data_file)
    if not os.path.exists(data_directory):
        os.makedirs(data_directory, exist_ok=True)
    # Use UTF-8 encoding to allow for Unicode characters to be written to the file
    with open(data_file, 'w', newline='', encoding='utf-8') as file:
        json.dump(document, file, sort_keys=True, indent=2)
    return 1


def read(data_file):
    """
    A helper function to read a JSON data file

    :param data_file: Path the data file to read
    :type data_file: str
    :return: Contents of the file as an object. Raises an exception when a read problem occurs.
    :rtype: dict
    """
    # Use UTF-8 encoding to be able to read Unicode characters
    with open(data_file, 'r', encoding='utf-8') as file:
        contents = json.load(file)
    return contents
