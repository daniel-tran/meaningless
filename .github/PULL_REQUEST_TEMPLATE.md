### Summary of changes
Provide either a list of items or a couple of short sentences describing the changes included in this pull request.

### General checklist
- [ ] All tests pass (without forcing any test to be successful) using these changes.
- [ ] Documentation is updated as needed. This includes both the "docs" folder and any markdown files.

### Translation checklist
If the pull request adds support for an additional Bible translation, confirm that the following items have been addressed:
- [ ] Add a new test case to `unit_tests_bible_translations.py` for the new translation
- [ ] Add all the necessary test data files under  `test\static\unit_tests_bible_translations`  in a new folder named according to the new translation.
- [ ] Add appropriate modifications to the Web Extractor (and relevant unit tests) to account for translation-specific components.
- [ ] Add appropriate modifications to the Base Downloader (and relevant unit tests) to specify any omitted passages in the translation.
