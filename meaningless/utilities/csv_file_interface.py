import os
import csv

# This is a collection of common methods used for interacting with CSV files.


def __get_header_list():
    """
    Returns the list of header fields prepended onto each CSV file.

    :return: The list of header fields.
    :rtype: str[]
    """
    return ['Book', 'Chapter', 'Passage', 'Text', 'Language', 'Translation', 'Copyright', 'Timestamp', 'Meaningless']


def write(data_file, document):
    """
    A helper function to write to a CSV data file.
    Note that the input data must adhere to the following conventions:

    1. The input document is a dictionary.
    2. There is a top-level key called 'Info', with string values for the following keys:
       'Language', 'Translation', 'Timestamp', 'Meaningless'
    3. There is at least one other top-level key-value pair, mapping to a dictionary of dictionaries.
    4. There are no keys or values with the value set as None (excluding the sub-keys under the top-level 'Info' key).

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
    # Use UTF-8-BOM encoding to allow for Unicode characters to be written to the file, but also display Unicode
    # characters correctly when viewing the data in certain spreadsheet applications
    with open(data_file, 'w', newline='', encoding='utf-8-sig') as file:
        csv_writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(__get_header_list())

        # Unlike other file interfaces, the metadata info is required to be provided by the input object.
        # This is to allow the CSV write function to determine the keys to access data for each row.
        if 'Info' not in document.keys():
            raise KeyError

        # Convert the mapping of info data into a list to make it easier to unpack the data on the CSV row
        info_fields = [document['Info'][info_field_key] for info_field_key in document['Info'].keys()]
        for book in document.keys():
            # The book name is not known, so obtain it by skipping all "non-book" keys
            if book in ['Info']:
                continue
            for chapter in document[book]:
                for passage in document[book][chapter]:
                    csv_writer.writerow([book, chapter, passage, document[book][chapter][passage], *info_fields])
    return 1


def read(data_file):
    """
    A helper function to read a CSV data file.
    Note that the file data must adhere to the following conventions:

    1. A header row is included as the first line.
    2. All data is contained within the first 8 columns.

    :param data_file: Path the data file to read
    :type data_file: str
    :return: Contents of the file as an object. Raises an exception when a read problem occurs.
    :rtype: dict
    """
    # Use UTF-8-BOM encoding to match the type used to write the file (assuming it was written with this file interface)
    output = {}
    with open(data_file, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file, fieldnames=__get_header_list())
        # Ignore the initial row of headers
        next(csv_reader)
        for row in csv_reader:
            book = row['Book']
            chapter = row['Chapter']
            passage = row['Passage']

            # Only assign the metadata once, since this should be the same on all rows anyway
            if 'Info' not in output:
                output['Info'] = {}
                for info_field_key in row.keys():
                    if info_field_key not in ['Book', 'Chapter', 'Passage', 'Text']:
                        output['Info'][info_field_key] = row[info_field_key]
            if book not in output:
                output[book] = {}
            if chapter not in output[book]:
                output[book][chapter] = {}
            if passage not in output[book][chapter]:
                output[book][chapter][passage] = row['Text']
    return output
