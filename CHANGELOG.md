# Change Log

## 1.3.0
- Added functionality to include minimal copyright information into the Base Extractor and Web Extractor
- Added Bible Gateway translation-specific copyright URL to output files
- Added translation support for: AMP, CSB, LSB, RSV

## 1.2.0
- Fixed an issue where the YAML Extractor sometimes includes extra whitespace that is not present in the Web Extractor
- Fixed an issue where the `output_as_list` flag in the Base Extractor would be modified when an error occurred while calling one of the text searching functions
- Drop library support for Python 3.9

## 1.1.0
- Fixed an issue where `get_passage_range` in the Web Extractor would incorrectly cap the upper limit of passages to 100
- Drop library support for Python 3.8
- Python version support now extends to the 4 earliest versions (subject to its EOL date) which are at least receiving security fixes

## 1.0.0
- Removed legacy_xml_file_interface module and the `use_legacy_mode` flag in the XML Downloader and Extractor
- Added experimental Apocrypha Web Extractor for the NRSVUE translation
- Added translation support for: NMB

## 0.7.0
- Refined xml_file_interface to use a more standard XML document structure with easier integration with XSLT
  - Added `use_legacy_mode` flag to XML Downloader and Extractor to continue using the original behaviour and assist with transitioning to the updated XML file interface
  - Added legacy_xml_file_interface module for backward compatibility with XML files using the previous (deprecated) document structure
- Added download timestamp and library version information to output files
- Drop library support for Python 3.7

## 0.6.1
- Fixed an issue where the JSON file interface was writing Unicode characters incorrectly to output files

## 0.6.0
- Added text searching functionality into Base Extractor
- Added a dedicated area for experimental functionality and helper scripts
  - With enough refinement, some of these might become new features in future releases
- Added translation support for: NRSVUE
- Removed translation support for: CJB

## 0.5.0
- Added CSV Extractor and CSV Downloader
- Added csv_file_interface module to assist with CSV file access
- Added translation support for: NIVUK
- Drop library support for Python 3.6

## 0.4.0
- Documentation is now publicly available through GitHub Pages. See https://daniel-tran.github.io/meaningless/
  - This was previously an undocumented change as part of the 0.3.0 release.
- Added XML Extractor and XML Downloader
- Added xml_file_interface module to assist with XML file access
- Added translation support for: RVA

## 0.3.0
- Added initial continuous integration workflow with GitHub Actions
- Added translation support for: BRG, CJB, EHV, ESVUK, GNV, GW, ISV, JUB, NASB1995, NOG
- Drop library support for Python 3.5

## 0.2.0
- Added Base Extractor, Base Downloader, JSON Extractor and JSON Downloader
  - Base Extractor contains shared logic for both the YAML and JSON Extractors
  - Base Downloader contains shared logic for both the YAML and JSON Downloaders
- Added json_file_interface module to assist with generic JSON file access
- Added translation support for: ASV, AKJV, KJ21, LEB, MEV, NET, NLV, YLT

## 0.1.0

- Initial release!
- Added Web Extractor, YAML Extractor and YAML Downloader
- Added yaml_file_interface module to assist with generic YAML file access
- Added translation support for: ESV, KJV, NASB, NIV, NKJV, NLT, NRSV, WEB
