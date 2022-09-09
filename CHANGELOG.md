# Change Log

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
