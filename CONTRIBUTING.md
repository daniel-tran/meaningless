# Setup
1. Fork the repo and clone it locally.
2. Setup a Python virtual environment.
3. Install the dependencies documented in `REQUIREMENTS.txt`.

# Running tests locally
If you are using PyCharm, you can run the tests within the IDE.

You can also run the tests on the command line. For example:
```bash
cd .\meaningless\test
python unit_tests_json_file_interface.py
```

# Code coverage
**Contributors should aim for about 90% statement and branch coverage**, although this is not strictly enforced.
So if you don't know how to use any of the available code coverage tools for Python, you can just concern yourself with writing suitable unit tests.

The currently recommended code coverage tool is [coverage.py ](https://github.com/nedbat/coveragepy), as it can show coverage results as a set of HTML pages and makes locating missed statements or branches in your unit tests rather intuitive.

# Submitting a change
1. **Check that all tests pass with your change**, in addition to any newly introduced tests.
2. Push your changes to your forked repo.
3. Create a pull request with your changes.
- Pull requests should be made against the current development branch, which is the version number.
- For consistency, the title should be prefixed with the version number followed by a colon.

Depending on the significance of your changes, it may be mentioned in `CHANGELOG.md` or `README.md`.

# Architecture
The following diagram represents the logical dependencies of each library component, and how changes in one component can propagate to others:
```
                                            Web Extractor
                                                  |
              --------------------------------------------------------------------------------
              |                       |                           |                          |
      YAML Downloader*         JSON Downloader*             XML Downloader*            CSV Downloader*
              |                       |                           |                          |
[YAML files only need to     [JSON files only need to     [XML files only need to     [CSV files only need to
   be downloaded once]          be downloaded once]          be downloaded once]         be downloaded once]
              |                       |                           |                          |
     YAML Extractor*           JSON Extractor*              XML Extractor*             CSV Extractor*
```

\* indicates that the component is a subclass of a base implementation, such as the Base Extractor or Base Downloader.

# Repository Layout
With reference to the directory contents:
- `meaningless`: This is where library components live.
- `meaningless\utilities`: This is where shared logic between components is housed.
- `test`: This is where the unit tests live.
- `test\static`: This is where static files used by unit tests are found. Create a new subdirectory for each test file except for the file interface test files.
- `test\tmp`: This is a temporary folder for unit tests that modify the working directory in some way.

# Performance Considerations
For the most part, performance is more or less sufficient as long as one uses standard Python techniques during development (e.g. list comprehensions, duck typing, etc.).

Implementation details specifically geared for performance optimisation, such as multithreading, would need to be assessed on whether the performance savings are significant enough to warrant inclusion without overcomplicating the code base more than necessary.

# Development Guide
Some parts of the library have a repeatable process for adding on new features and such, which are documented below:

## Supporting a new translations
- Add a new translation code to the appropriate method under `meaningless\utilities\common.py`.
- Add a new test case to `system_tests_bible_translations.py` for the new translation. This is used to validate end-to-end correctness.
  - Add all the necessary test data files under `test\static\system_tests_bible_translations` in a new folder named according to the new translation. You can use the helper script under `experimental\system_test_helper.py` to make this process easier.
- Make appropriate modifications to the Web Extractor to account for translation-specific components, such as double spaces and in-line translation notes.
  - Add unit tests for the Web Extractor to test these specific changes.
  - Run all the Web Extractor unit tests to ensure stable behaviour with said changes.
- Add appropriate modifications to the Base Downloader to specify any omitted passages that are present in the new translation.
  - Update the relevant test case in `system_tests_bible_translations.py` to check for correct handling of omitted passages.

## Adding a new extractor or downloader
- Add a new file interface under `meaningless\utilities` with the following two standalone methods:
  - `def write(data_file, document)`
    - `data_file` is a string corresponding to the file path to write to.
    - `document` is a dictionary with the structure shown below.
    - Returns 1 when successful.
  - `def read(data_file)`
    - `data_file` is a string corresponnding to the file path to read.
    - Returns a dictionary with the structure shown below.
- Add unit tests for the new file interface.
- Add a new extractor or downloader class which extends the BaseExtractor class, passing in the appropriate function for reading or writing.

This is the dictionary structure that is passed into `write` and returned from `read`:

```json
{
  "Book Name": {
    "Chapter Number 1": {
      "Passage Number 1": "Passage Contents 1",
      ...
      "Passage Number N": "Passage Contents N"
    },
    ...
    "Chapter Number N": {
      "Passage Number 1": "Passage Contents 1",
      ...
      "Passage Number N": "Passage Contents N"
    }
  },
  "Info": {
    "Language": "Translation Language",
    "Translation": "Translation Code"
  }
}
```
