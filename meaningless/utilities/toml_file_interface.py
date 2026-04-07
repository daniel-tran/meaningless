import os
try:
    import tomli
    import tomli_w
except ImportError:
    # Fallback for Python 3.11+ which has tomllib in standard library
    try:
        import tomllib as tomli
    except ImportError:
        tomli = None
    try:
        import tomli_w
    except ImportError:
        tomli_w = None

# This is a collection of common methods used for interacting with TOML files.


def write(data_file, document):
    """
    A helper function to write to a TOML data file.

    :param data_file: Path to the data file to write to
    :type data_file: str
    :param document: In-memory TOML structure, usually a dictionary
    :type document: dict
    :return: Returns 1 on success. Raises an exception when a write problem occurs.
    :rtype: int
    """
    if tomli_w is None:
        raise ImportError("tomli_w library is required for writing TOML files")
    
    # Only create the directory if it doesn't already exist. This is also to account for directories which are the
    # top level of a given drive (e.g. C:/) which can't be created by the file system due to denied access.
    data_directory = os.path.dirname(data_file)
    if not os.path.exists(data_directory):
        os.makedirs(data_directory, exist_ok=True)
    
    # Convert document to proper TOML structure if needed
    def convert_keys_to_strings(obj):
        """Recursively convert integer keys to strings for TOML compatibility"""
        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                # Convert integer keys to strings
                if isinstance(key, int):
                    result[str(key)] = convert_keys_to_strings(value)
                else:
                    result[key] = convert_keys_to_strings(value)
            return result
        elif isinstance(obj, list):
            return [convert_keys_to_strings(item) for item in obj]
        else:
            return obj
    
    toml_document = document
    if isinstance(document, str):
        # Convert string to a simple TOML structure
        toml_document = {"content": document}
    elif isinstance(document, list):
        # Convert list to a simple TOML structure
        toml_document = {"items": document}
    else:
        # Convert any integer keys to strings for TOML compatibility
        toml_document = convert_keys_to_strings(document)
    
    # Use UTF-8 encoding to allow for Unicode characters to be written to the file
    with open(data_file, 'wb') as file:
        tomli_w.dump(toml_document, file)
    return 1


def read(data_file):
    """
    A helper function to read a TOML data file

    :param data_file: Path the data file to read
    :type data_file: str
    :return: Contents of the file as an object. Raises an exception when a read problem occurs.
    :rtype: dict
    """
    if tomli is None:
        raise ImportError("tomli library is required for reading TOML files")
    
    # Use UTF-8 encoding to be able to read Unicode characters
    with open(data_file, 'rb') as file:
        contents = tomli.load(file)
    return contents