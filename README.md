[![Test Status](https://github.com/daniel-tran/meaningless/actions/workflows/run_tests.yaml/badge.svg)](https://github.com/daniel-tran/meaningless/actions/workflows/run_tests.yaml)

Meaningless is a Python library used to retrieve, process and download Bible passages from Bible Gateway.

Features include:
- Passage retrieval from the [Bible Gateway](https://www.biblegateway.com) site or from a local YAML/JSON/XML/CSV file.
- Different output formats for different purposes:
  - Multi-line strings for printing Bible passages.
  - Python list of strings (or in-memory data structure) for passing Bible passages to other Python logic.
  - YAML/JSON/XML/CSV files for persistent storage of Bible passages or as input for other applications and scripts.
- Handling of edge case passages, such as those with tabular data and omitted passages in certain translations.
- Flags to enable particular content modifications, such as ignoring passage numbers.

**Now accepting feature requests!** If you want to see a certain feature included, please create an issue describing all the necessary details.

# Installation

```
pip install meaningless
```

# API Documentation

Documentation is generated using Sphinx.

## Online

The API documentation is hosted through GitHub Pages at the following link: https://daniel-tran.github.io/meaningless/

## Offline

You can view the API documentation as static HTML documents from `docs\index.html`. After cloning this repo, you can load the HTML files in a web browser, which allows you to navigate to other sections.

# Supported translations

## English

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
- NIVUK
- NKJV
- NLT
- NLV
- NOG
- NRSV
- WEB
- YLT

## Español

- RVA

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

## XML Downloader
The XML Downloader is effectively the same as the YAML Downloader except the resulting file is in a specific XML format and has a different file extension.
```python
from meaningless import XMLDownloader

if __name__ == '__main__':
    downloader = XMLDownloader()
    downloader.download_passage('Ecclesiastes', 1, 2)
```
Output:

Running the above code would produce a file called `Ecclesiastes.xml` in the current working directory with the following contents:
```xml
<?xml version="1.0" encoding="utf-8"?>
<root>
  <Info>
    <Language>English</Language>
    <Translation>NIV</Translation>
  </Info>
  <Ecclesiastes>
    <_1>
      <_2>² “Meaningless! Meaningless!”
    says the Teacher.
“Utterly meaningless!
    Everything is meaningless.”</_2>
    </_1>
  </Ecclesiastes>
</root>
```

Note that the following adjustments are made to the downloaded contents to ensure it is a well-formed XML document:

1. A top-level "root" tag is present.
2. All tag names starting with a number are prefixed.
3. Tags corresponding to book names use a placeholder character for spaces.

## XML Extractor
Much like the YAML Extractor, the XML Extractor uses the generated files from the XML Downloader to find passages.
```python
from meaningless import XMLExtractor

if __name__ == '__main__':
    bible = XMLExtractor()
    passage = bible.get_passage('Ecclesiastes', 1, 2)
    print(passage)
```
Output:

Assuming the XML downloader has already generated a XML file in the current directory called `Ecclesiastes.xml` which contains the book of Ecclesiastes in XML format:
```
² “Meaningless! Meaningless!”
    says the Teacher.
“Utterly meaningless!
    Everything is meaningless.”
```

## XML File Interface
The XML File Interface is a set of helper methods used to read and write XML files. Unlike the other file interfaces, this is more geared towards the XML document format used by the XML Downloader and Extractor, so you may observe some strange behaviour if you try using this for general purpose XML file interactions.
```python
from meaningless import XMLDownloader, xml_file_interface

if __name__ == '__main__':
    downloader = XMLDownloader()
    downloader.download_passage('Ecclesiastes', 1, 2)
    bible = xml_file_interface.read('./Ecclesiastes.xml')
    bible['Info']['Customised'] = True
    xml_file_interface.write('./Ecclesiastes.xml', bible)
```
Output:

Running the above code would produce a file called `Ecclesiastes.xml` in the current working directory with the following contents:
```xml
<?xml version="1.0" encoding="utf-8"?>
<root>
  <Info>
    <Language>English</Language>
    <Translation>NIV</Translation>
    <Customised>true</Customised>
  </Info>
  <Ecclesiastes>
    <_1>
      <_2>² “Meaningless! Meaningless!”
    says the Teacher.
“Utterly meaningless!
    Everything is meaningless.”</_2>
    </_1>
  </Ecclesiastes>
</root>
```

**Note that you allowed to write badly formed XML documents using this file interface, but they will cause runtime errors in your code upon trying to read and process them.**

## CSV Downloader
The CSV Downloader is effectively the same as the YAML Downloader except the resulting file is in CSV format and has a different file extension.
```python
from meaningless import CSVDownloader

if __name__ == '__main__':
    downloader = CSVDownloader()
    downloader.download_passage('Ecclesiastes', 1, 2)
```
Output:

Running the above code would produce a file called `Ecclesiastes.csv` in the current working directory with the following contents:
```
Book,Chapter,Passage,Text,Language,Translation
Ecclesiastes,1,2,"² “Meaningless! Meaningless!”
    says the Teacher.
“Utterly meaningless!
    Everything is meaningless.”",English,NIV
```

## CSV Extractor
Much like the YAML Extractor, the CSV Extractor uses the generated files from the CSV Downloader to find passages.
```python
from meaningless import CSVExtractor

if __name__ == '__main__':
    bible = CSVExtractor()
    passage = bible.get_passage('Ecclesiastes', 1, 2)
    print(passage)
```
Output:

Assuming the CSV downloader has already generated a CSV file in the current directory called `Ecclesiastes.csv` which contains the book of Ecclesiastes in CSV format:
```
² “Meaningless! Meaningless!”
    says the Teacher.
“Utterly meaningless!
    Everything is meaningless.”
```

## CSV File Interface
The CSV File Interface is a set of helper methods used to read and write CSV files. Like the XML File Interface, this is geared towards the CSV document format used by the CSV Downloader and Extractor and cannot be used to add custom attributes to the output file when writing CSV data.
```python
from meaningless import CSVDownloader, csv_file_interface

if __name__ == '__main__':
    downloader = CSVDownloader()
    downloader.download_passage('Ecclesiastes', 1, 2)
    bible = csv_file_interface.read('./Ecclesiastes.csv')
    bible['Info']['Language'] = 'English (EN)'
    csv_file_interface.write('./Ecclesiastes.csv', bible)
```
Output:

Running the above code would produce a file called `Ecclesiastes.csv` in the current working directory with the following contents:
```
Book,Chapter,Passage,Text,Language,Translation
Ecclesiastes,1,2,"² “Meaningless! Meaningless!”
    says the Teacher.
“Utterly meaningless!
    Everything is meaningless.”",English (EN),NIV
```

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

To make a contribution to this library, refer to `CONTRIBUTING.md`.
