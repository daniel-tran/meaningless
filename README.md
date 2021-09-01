[![Test Status](https://github.com/daniel-tran/meaningless/actions/workflows/run_tests.yaml/badge.svg)](https://github.com/daniel-tran/meaningless/actions/workflows/run_tests.yaml)

Meaningless is a Python library used to retrieve, process and download Bible passages from Bible Gateway.

Features include:
- Passage retrieval from the [Bible Gateway](https://www.biblegateway.com) site or from a local YAML/JSON file.
- Different output formats for different purposes:
  - Multi-line strings for printing Bible passages.
  - Python list of strings (or in-memory data structure) for passing Bible passages to other Python logic.
  - YAML/JSON files for persistent storage of Bible passages.
- Handling of edge case passages, such as those with tabular data and omitted passages in certain translations.
- Flags to enable particular content modifications, such as ignoring passage numbers.

**Now accepting feature requests!** If you want to see a certain feature included, please create an issue describing all the nececssary details.

# Supported translations

- ASV
- AKJV
- BRG
- CJB
- EHV
- ESV
- ESVUK
- GNV
- GW
- ISV
- JUB
- KJV
- KJ21
- LEB
- MEV
- NASB
- NASB1995
- NET
- NIV
- NKJV
- NLT
- NLV
- NOG
- NRSV
- WEB
- YLT

# Installation

```
pip install meaningless
```

# Usage

## Web Extractor
The Web Extractor is used to obtain passage information directly from [Bible Gateway](https://www.biblegateway.com).
```python
from meaningless import WebExtractor

if __name__ == '__main__':
    bible = WebExtractor()
    passage = bible.get_passage('Ecclesiastes', 1, 2)
    print(passage)
```
Output:
```
² “Meaningless! Meaningless!”
    says the Teacher.
“Utterly meaningless!
    Everything is meaningless.”
```

## YAML Downloader
The YAML Downloader is which formats passages obtained from the Bible Gateway website (using the Web Extractor) into a YAML structure and writes it out to a file:
```python
from meaningless import YAMLDownloader

if __name__ == '__main__':
    downloader = YAMLDownloader()
    downloader.download_passage('Ecclesiastes', 1, 2)
```
Output:

Running the above code would produce a file called `Ecclesiastes.yaml` in the current working directory with the following contents:
```
Ecclesiastes:
  1:
    2: "² “Meaningless! Meaningless!”\n    says the Teacher.\n“Utterly meaningless!\n\
      \    Everything is meaningless.”"
Info:
  Language: English
  Translation: NIV
```

## YAML Extractor
The YAML Extractor uses the generated files from the YAML Downloader to find passages. This is faster than the Web Extractor, since it is not retrieving information from the Internet and is also unaffected by bandwidth limitations.
```python
from meaningless import YAMLExtractor

if __name__ == '__main__':
    bible = YAMLExtractor()
    passage = bible.get_passage('Ecclesiastes', 1, 2)
    print(passage)
```
Output:

Assuming the YAML downloader has already generated a YAML file in the current directory called `Ecclesiastes.yaml` which contains the book of Ecclesiastes in YAML format:
```
² “Meaningless! Meaningless!”
    says the Teacher.
“Utterly meaningless!
    Everything is meaningless.”
```

## YAML File Interface
The YAML File Interface is a set of helper methods used to read and write YAML files. This can be useful if you need to do some customised processing on a downloaded YAML file.
```python
from meaningless import YAMLDownloader, yaml_file_interface

if __name__ == '__main__':
    downloader = YAMLDownloader()
    downloader.download_passage('Ecclesiastes', 1, 2)
    bible = yaml_file_interface.read('./Ecclesiastes.yaml')
    bible['Info']['Customised?'] = True
    yaml_file_interface.write('./Ecclesiastes.yaml', bible)
```
Output:

Running the above code would produce a file called `Ecclesiastes.yaml` in the current working directory with the following contents:
```python
Ecclesiastes:
  1:
    2: "² “Meaningless! Meaningless!”\n    says the Teacher.\n“Utterly meaningless!\n\
      \    Everything is meaningless.”"
Info:
  Language: English
  Translation: NIV
  Customised?: true
```

## JSON Downloader
The JSON Downloader is effectively the same as the YAML Downloader except the resulting file is in JSON format and has a different file extension.
```python
from meaningless import JSONDownloader

if __name__ == '__main__':
    downloader = JSONDownloader()
    downloader.download_passage('Ecclesiastes', 1, 2)
```
Output:

Running the above code would produce a file called `Ecclesiastes.json` in the current working directory with the following contents:
```
{
  "Ecclesiastes": {
    "1": {
      "2": "\u00b2 \u201cMeaningless! Meaningless!\u201d\n    says the Teacher.\n\u201cUtterly meaningless!\n    Everything is meaningless.\u201d"
    }
  },
  "Info": {
    "Language": "English",
    "Translation": "NIV"
  }
}
```

## JSON Extractor
Much like the YAML Extractor, the JSON Extractor uses the generated files from the JSON Downloader to find passages.
```python
from meaningless import JSONExtractor

if __name__ == '__main__':
    bible = JSONExtractor()
    passage = bible.get_passage('Ecclesiastes', 1, 2)
    print(passage)
```
Output:

Assuming the JSON downloader has already generated a JSON file in the current directory called `Ecclesiastes.json` which contains the book of Ecclesiastes in JSON format:
```
² “Meaningless! Meaningless!”
    says the Teacher.
“Utterly meaningless!
    Everything is meaningless.”
```

## JSON File Interface
The JSON File Interface is a set of helper methods used to read and write JSON files. Similar to the YAML File Interface, it can be used to do customised processing on a JSON file or its contents.
```python
from meaningless import JSONDownloader, json_file_interface

if __name__ == '__main__':
    downloader = JSONDownloader()
    downloader.download_passage('Ecclesiastes', 1, 2)
    bible = json_file_interface.read('./Ecclesiastes.json')
    bible['Info']['Customised?'] = True
    json_file_interface.write('./Ecclesiastes.json', bible)
```
Output:

Running the above code would produce a file called `Ecclesiastes.json` in the current working directory with the following contents:
```python
{
  "Ecclesiastes": {
    "1": {
      "2": "\u00b2 \u201cMeaningless! Meaningless!\u201d\n    says the Teacher.\n\u201cUtterly meaningless!\n    Everything is meaningless.\u201d"
    }
  },
  "Info": {
    "Customised?": true,
    "Language": "English",
    "Translation": "NIV"
  }
}
```

# API Documentation
To view the available classes and methods in this library, you can view them as static HTML documents from `docs\release\index.html`. After cloning this repo, you can load the HTML files in a web browser, which allows you to navigate to other sections.
These files were generated using Sphinx.

# Q&A

## How to report potential bugs and other feedback?

To report bugs and other problems, create an issue in this repo that details:
- A brief description of the problem encountered
- Steps to recreate the problem (or a code sample that demonstrates the problem)
- Expected result
- The version of this library being used

If you have any questions, complaints, compliments or even ideas to improve this library, you can also leave them as a GitHub issue with the appropriate label.
Or you can also send an email to [dantran.au@gmail.com](mailto:dantran.au@gmail.com), although a response will likely take longer than replying to a GitHub issue.

## Should I manually edit the downloaded file?

**This is NOT recommended** under normal circumstances, as it may cause problems with the library API when using the modified file.

## What's the process for supporting new translations?

- Add a new test case to `unit_tests_bible_translations.py` for the new translation. This is used to validate end-to-end correctness.
  - Add all the necessary test data files under `test\static\unit_tests_bible_translations` in a new folder named according to the new translation.
- Make appropriate modifications to the Web Extractor to account for translation-specific components, such as double spaces and in-line translation notes.
  - Add unit tests for the Web Extractor to test these specific changes.
  - Run all the Web Extractor unit tests to ensure stable behaviour with said changes.
- Add appropriate modifications to the Base Downloader to specify any omitted passages that are present in the new translation.
  - Update the relevant test case in `unit_tests_bible_translations.py` to check for correct handling of omitted passages.

## If multiple translations are supported, why aren't there more unit tests for these?

The Base Extractor and Downloader all use the same overall structure to represent passage contents for all translations.

For the Web Extractor, the page structure of the [Bible Gateway](https://www.biblegateway.com) site is mostly the same across different translations, so as long as the translation-specific differences are handled correctly, the same set of unit tests should suffice.

## Will this library ever drop support for certain translations?

Short answer: It depends.

The primary case for dropping support for a certain Bible translation is if there is an observed problem in the extracted Bible contents which is considerably difficult to address due to how the Biblical contents is structured (in terms of HTML) on the [Bible Gateway](https://www.biblegateway.com) site. With that in mind, reinstating support for Bible translations can be reconsidered when such problems subside.

## How are omitted passages determined for each translation?

Without having to go through every single passage and check if it is omitted, a set of common omitted passages are found here: 
- https://en.wikipedia.org/wiki/List_of_New_Testament_verses_not_included_in_modern_English_translations
- http://textus-receptus.com/wiki/List_of_Omitted_Bible_Verses#List_of_Bible_verses_totally_omitted

These passages are checked on the [Bible Gateway](https://www.biblegateway.com) site, and then added to the Base Downloader's internal list of omitted passages for the relevant translation.

If you notice any problems such as unhandled omitted passages or incorrect tagging of an omitted passage in the Base Downloader, please create an issue to report it.

## Does this library provide support for the Apocrypha books?

At the moment, you can use the Web Extractor's `search()` and `search_multiple()` functions to obtain passages from the Apocrypha books.
There is currently no official support for the Apocrypha books in the other downloaders and extractors, at least until proper use cases can be identified.

# Contributors
- [daniel-tran](https://github.com/daniel-tran) (Creator & current maintainer)

To make a contribution to this library, refer to `DEVELOPMENT.md`.
