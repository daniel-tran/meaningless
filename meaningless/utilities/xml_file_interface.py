import re
import os
import xmltodict

# This is a collection of common methods used for interacting with XML files.


def __get_root_name():
    """
    Gets the top-level tag name used in the document.

    :return: Returns the tag name.
    :rtype: str
    """
    return 'root'


def __get_book_name():
    """
    Gets the tag name used for books in the document.

    :return: Returns the tag name.
    :rtype: str
    """
    return 'book'


def __get_chapter_name():
    """
    Gets the tag name used for chapters in the document.

    :return: Returns the tag name.
    :rtype: str
    """
    return 'chapter'


def __get_passage_name():
    """
    Gets the tag name used for passages in the document.

    :return: Returns the tag name.
    :rtype: str
    """
    return 'passage'


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


def __restore_xml_key_and_value(path, key, value):
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
    # Most keys can be reverted back to their original case, as XML conventions no longer apply
    if new_key not in [__get_root_name()]:
        new_key = new_key.title()
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

    1. If a top-level key is named 'Info', it must be a mapping of string keys to string values.
    2. All other top-level keys map to a 3-layer dictionary or similar data structure with key-value pairs.
    3. The 3rd layer of this data structure is a mapping of string keys to string values.

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

    modified_document = {__get_root_name(): {}}
    for key in list(document.keys()):
        # Copy in all the "non-book" information as is
        if key in ['Info']:
            # Convert all immediate keys to lowercase, which is the general XML convention
            new_key = key.lower()
            modified_document[__get_root_name()][new_key] = {}
            for sub_key in document[key]:
                modified_document[__get_root_name()][new_key][sub_key.lower()] = document[key][sub_key]
            continue

        # The XML output should provide some supplementary metadata for use in the read() function
        # Note that the leading prefix is only required for book names which start with a number, but add it in
        # all cases anyway for simpler logic.
        modified_document[__get_root_name()][__get_book_name()] = {
            '@name': key,
            '@tag': f'{__get_space_placeholder()}{key.replace(" ", __get_space_placeholder())}',
            __get_chapter_name(): []
        }
        for chapter in list(document[key].keys()):
            modified_document[__get_root_name()][__get_book_name()][__get_chapter_name()].append({
                '@number': chapter,
                '@tag': f'{__get_numeric_prefix()}{chapter}',
                __get_passage_name(): []
            })
            for passage in list(document[key][chapter].keys()):
                # Avoid potential unparsing errors by always casting the passage content as a string
                modified_document[__get_root_name()][__get_book_name()][__get_chapter_name()][-1][__get_passage_name()]\
                    .append({
                        '@number': passage,
                        '@tag': f'{__get_numeric_prefix()}{passage}',
                        '#text': str(document[key][chapter][passage])
                    })
    # Use space indentation, to keep in line with most of the other file interfaces
    contents = xmltodict.unparse(modified_document, pretty=True, indent='  ')
    # Use UTF-8 encoding to allow for Unicode characters to be written to the file
    with open(data_file, 'w', newline='', encoding='utf-8') as file:
        file.write(contents)
    return 1


def read(data_file):
    """
    A helper function to read a XML data file.
    Note that the input data must adhere to the following conventions:

    1. The top-level tag is called 'root'.
    2. All <book> tags must have a "tag" attribute.
    3. All <chapter> tags must have a "tag" attribute and must be nested within a <book> tag.
    4. All <passage> tags must have a "tag" attribute and must be nested within a <chapter> tag.

    If the XML data file is valid, the returned object will differ from the XML data file in the following ways:

    1. Leading and trailing underscores will be removed.
    2. All other underscores will be converted into spaces.
    3. All keys will be converted to title case (all first letters of each word are capitalised)

    :param data_file: Path to the data file to read
    :type data_file: str
    :return: Contents of the file as an object. Raises an exception when a read problem occurs.
    :rtype: dict
    """
    # Use UTF-8 encoding to be able to read Unicode characters
    with open(data_file, 'r', encoding='utf-8') as file:
        contents = file.read()
    # Pre-process the XML contents such that when it gets parsed, it is mostly in the expected structure
    # that file interfaces are to operate by.
    #
    # This works by pre-computing the relevant object keys as XML-compliant values when writing
    # the file and restoring that value as the preferred tag name when reading it back.
    # After parsing, it's necessary to do some post-processing on the document again, as most of the
    # XML-compliant modifications are only needed to pass the underlying XML validation checks.
    tags_with_predefined_replacements = [__get_book_name(), __get_chapter_name(), __get_passage_name()]
    for tag in tags_with_predefined_replacements:
        contents = re.sub(fr'<{tag}\s*.*?\s*tag="(.+?)">(.*?)</{tag}>', r'<\1>\2</\1>',
                          contents, flags=re.DOTALL)
    # Since white space and newlines are preserved, the side effect is that a cdata key is automatically added into
    # each level of the document, with its value being spaces and newline characters.
    raw_document = xmltodict.parse(contents, strip_whitespace=False, cdata_key=__get_cdata_key(),
                                   postprocessor=__restore_xml_key_and_value)
    return raw_document[__get_root_name()]
