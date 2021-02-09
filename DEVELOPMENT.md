# Setup
1. Fork the repo and clone it locally.
2. Setup a Python virtual environment.
3. Install the dependencies documented in `REQUIREMENTS.txt`.

# Submitting a change
1. **Check that all tests pass with your change**, in addition to any newly introduced tests.
2. Add a description of your change to `CHANGELOG.md`.
3. Push your changes to your forked repo.
4. Create a pull request with your changes. You can also add yourself to the Contributors list in `README.md`.

# Architecture
The following diagram represents the logical dependencies of each library component, and how changes in one component can propagate to others:
```
                                        Web Extractor
                                              |
                                  -------------------------
                                  |                       |
                          YAML Downloader*         JSON Downloader*
                                  |                       |
                    [YAML files only need to     [JSON files only need to
                       be downloaded once]          be downloaded once]
                                  |                       |
                         YAML Extractor*           JSON Extractor*
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
