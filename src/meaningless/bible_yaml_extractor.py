import os
from ruamel.yaml import YAML
from ruamel.yaml.parser import ParserError


def __read_yaml_file(data_file):
    """
    A helper function to read a YAML data file
    :param data_file: Path the data file to read
    :return: Contents of the file
    """
    contents = []

    # Easier to proactively detect non-existent YAML file than to rely on reactive exception handling
    if not os.path.exists(data_file):
        print('WARNING: "{0}" does not exist'.format(data_file))
        return contents

    try:
        # Use UTF-8 encoding to be able to read Unicode characters
        with open(data_file, 'r', encoding='utf-8') as file:
            loader = YAML(typ="safe")  # 'Safe' means it won't load unknown tags
            contents = loader.load(file)
        file.close()
    except ParserError:
        # Exception handling requires importing explicit components under ruamel.yaml
        print('WARNING: "{0}" does not contain valid YAML syntax'.format(data_file))
    return contents


def __get_module_directory():
    """
    A helper function to retrieve the directory of the module & ensure YAML files can be read without path modifications
    :return: The directory to the folder that contains this Python source file
    """
    return os.path.dirname(__file__)


def get_yaml_passage(book, chapter, passage):
    """
    Gets a single passage from the YAML Bible files
    :param book: Name of the book
    :param chapter: Chapter number
    :param passage: Passage number
    :return: The passage as text
    """
    return get_yaml_passage_range(book, chapter, passage, chapter, passage)


def get_yaml_passages(book, chapter, passage_from, passage_to):
    """
    Gets a range of passages of the same chapter from the YAML Bible files
    :param book: Name of the book
    :param chapter: Chapter number
    :param passage_from: First passage number to get
    :param passage_to: Last passage number to get
    :return: The passages between passage_from and passage_to (inclusive) as text
    """
    return get_yaml_passage_range(book, chapter, passage_from, chapter, passage_to)


def get_yaml_chapter(book, chapter):
    """
    Gets a single chapter from the YAML Bible files
    :param book: Name of the book
    :param chapter: Chapter number
    :return: All passages in the chapter as text
    """
    translation = 'NIV'
    document = __read_yaml_file('{0}/{1}/{2}.yaml'.format(__get_module_directory(), translation, book))
    chapter_length = len(document[book][chapter].keys())
    return get_yaml_passage_range(book, chapter, 1, chapter, chapter_length)


def get_yaml_chapters(book, chapter_from, chapter_to):
    """
    Gets a range of passages from a specified chapters selection from the YAML Bible files
    :param book: Name of the book
    :param chapter_from: First chapter number to get
    :param chapter_to: Last chapter number to get
    :return: All passages between chapter_from and chapter_to (inclusive) as text
    """
    translation = 'NIV'
    document = __read_yaml_file('{0}/{1}/{2}.yaml'.format(__get_module_directory(), translation, book))
    chapter_to_length = len(document[book][chapter_to].keys())
    return get_yaml_passage_range(book, chapter_from, 1, chapter_to, chapter_to_length)


def get_yaml_passage_range(book, chapter_from, passage_from, chapter_to, passage_to):
    """
    Gets a range of passages from one specific passage to another passage from the YAML Bible files
    :param book: Name of the book
    :param chapter_from: First chapter number to get
    :param passage_from: First passage number to get in the first chapter
    :param chapter_to: Last chapter number to get
    :param passage_to: Last passage number to get in the last chapter
    :return: All passages between the two passages (inclusive) as text
    """
    translation = 'NIV'
    # Use __file__ to ensure the file is read relative to the module location
    document = __read_yaml_file('{0}/{1}/{2}.yaml'.format(__get_module_directory(), translation, book))
    passage_list = []
    # Extend the range by 1 since chapter_to is also included in the iteration
    for chapter in range(chapter_from, chapter_to + 1):
        # Determine the range of passages to extract from the chapter
        passage_initial = 1
        passage_final = len(document[book][chapter].keys())
        if chapter == chapter_from:
            # For the first chapter, an initial set of passages can be ignored (undercuts the passage selection)
            passage_initial = passage_from
        if chapter == chapter_to:
            # For the last chapter, a trailing set of passages can be ignored (exceeds the passage selection)
            passage_final = passage_to
        # Extend the range by 1 since the last passage is also included in the iteration
        [passage_list.append(document[book][chapter][passage]) for passage in range(passage_initial, passage_final + 1)]
        # Start each chapter on a new line
        passage_list.append('\n')
    # Convert the list of passages into a string, as strings are immutable and manually re-initialising a new string
    # in the loop can be costly to performance.
    return ''.join([passage for passage in passage_list]).strip()


if __name__ == "__main__":
    # Run this section when run as a standalone script. Don't run this part when being imported.
    print('Oink')
