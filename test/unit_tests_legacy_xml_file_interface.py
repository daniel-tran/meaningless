import unittest
import sys
import xml
sys.path.append('../')
from meaningless import legacy_xml_file_interface


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    @staticmethod
    def get_static_file(filename):
        return './static/unit_tests_legacy_xml_file_interface/{0}'.format(filename)

    @staticmethod
    def get_temp_file(filename):
        return './tmp/unit_tests_legacy_xml_file_interface/{0}'.format(filename)

    def test_read(self):
        document = legacy_xml_file_interface.read(self.get_static_file('test_read.xml'))
        self.assertEqual(list(document.keys()), ['Disco'], 'Main keys are incorrect')
        self.assertEqual(document['Disco']['Beatdown'], '1', 'First entry is incorrect')
        self.assertEqual(document['Disco']['Elysium'], '2', 'Second entry is incorrect')

    def test_write(self):
        document = {'Disco': {'1': 'Beatdown', '2': 'Elysium'}}
        filename = 'test_write.xml'
        legacy_xml_file_interface.write(self.get_temp_file(filename), document)
        # Mainly testing for file contents, ignoring other details like encoding and line endings
        self.assertEqual(legacy_xml_file_interface.read(self.get_static_file(filename)),
                         legacy_xml_file_interface.read(self.get_temp_file(filename)), 'Files do not match')

    def test_write_overwrite(self):
        filename = 'test_write_overwrite.xml'
        document = {'Disco': {'1': 'Beatdown', '2': 'Elysium'}}
        legacy_xml_file_interface.write(self.get_temp_file(filename), document)
        document['Disco']['3'] = 'Fever'
        legacy_xml_file_interface.write(self.get_temp_file(filename), document)
        # Assert that the file has been modified according to the latest changes
        modified_document = legacy_xml_file_interface.read(self.get_temp_file(filename))
        self.assertEqual(len(modified_document['Disco']), 3, 'Number of entries is incorrect')
        self.assertEqual(modified_document['Disco']['3'], 'Fever', 'Third entry is incorrect')

    def test_read_with_space_placeholders_in_top_level_key(self):
        document = legacy_xml_file_interface.read(
            self.get_static_file('test_read_with_space_placeholders_in_top_level_key.xml'))
        self.assertEqual(list(document.keys()), ['Disc o'], 'Main keys are incorrect')
        self.assertEqual(document['Disc o']['Beatdown'], '1', 'First entry is incorrect')
        self.assertEqual(document['Disc o']['Elysium'], '2', 'Second entry is incorrect')

    def test_write_with_spaces_in_top_level_key(self):
        document = {'Disc o': {'Beatdown': '1', 'Elysium': '2'}}
        filename = 'test_write_with_spaces_in_top_level_key.xml'
        legacy_xml_file_interface.write(self.get_temp_file(filename), document)
        # Mainly testing for file contents, ignoring other details like encoding and line endings
        self.assertEqual(legacy_xml_file_interface.read(self.get_static_file(filename)),
                         legacy_xml_file_interface.read(self.get_temp_file(filename)), 'Files do not match')

    def test_read_with_number_prefixed_top_level_key(self):
        document = legacy_xml_file_interface.read(self.get_static_file('test_read_with_number_prefixed_top_level_key.xml'))
        self.assertEqual(list(document.keys()), ['1 Disco'], 'Main keys are incorrect')
        self.assertEqual(document['1 Disco']['Beatdown'], '1', 'First entry is incorrect')
        self.assertEqual(document['1 Disco']['Elysium'], '2', 'Second entry is incorrect')

    def test_write_with_number_prefixed_top_level_key(self):
        document = {'1 Disco': {'Beatdown': '1', 'Elysium': '2'}}
        filename = 'test_write_with_number_prefixed_top_level_key.xml'
        legacy_xml_file_interface.write(self.get_temp_file(filename), document)
        # Mainly testing for file contents, ignoring other details like encoding and line endings
        self.assertEqual(legacy_xml_file_interface.read(self.get_static_file(filename)),
                         legacy_xml_file_interface.read(self.get_temp_file(filename)), 'Files do not match')

    def test_write_with_number_top_level_key(self):
        filename = 'test_write_with_number_top_level_key.xml'
        document = {1: {'Beatdown': 1, 'Elysium': 2}}
        legacy_xml_file_interface.write(self.get_temp_file(filename), document)
        result = legacy_xml_file_interface.read(self.get_temp_file(filename))
        self.assertEqual(result['1']['Beatdown'], '1', 'First entry is incorrect')
        self.assertEqual(result['1']['Elysium'], '2', 'Second entry is incorrect')

    def test_read_with_number_prefixed_second_level_key(self):
        filename = 'test_read_with_number_prefixed_second_level_key.xml'
        document = legacy_xml_file_interface.read(self.get_static_file(filename))
        self.assertEqual(document['Disco']['1'], 'Beatdown', 'First entry is incorrect')
        self.assertEqual(document['Disco']['2'], 'Elysium', 'Second entry is incorrect')

    def test_read_nonexistent_file(self):
        self.assertRaises(FileNotFoundError, legacy_xml_file_interface.read,
                          self.get_static_file('test_read_nonexistent_file.xml'))

    def test_write_string_contents(self):
        document = 'Ugh'
        filename = self.get_temp_file('test_write_string_contents.xml')
        # XML file interface only supports data structures with keys
        self.assertRaises(AttributeError, legacy_xml_file_interface.write, filename, document)

    def test_write_list_contents(self):
        document = ['Disco', 'Fever']
        filename = self.get_temp_file('test_write_list_contents.xml')
        # XML file interface only supports data structures with keys
        self.assertRaises(AttributeError, legacy_xml_file_interface.write, filename, document)

    def test_read_path_exceeds_windows_limit(self):
        filename = '{0}.xml'.format('G' * 255)
        self.assertRaises((FileNotFoundError, OSError), legacy_xml_file_interface.read,
                          self.get_static_file(filename))

    def test_write_path_exceeds_windows_limit(self):
        document = {'Disco': 7}
        filename = './tmp/{0}.xml'.format('G' * 255)
        self.assertRaises((FileNotFoundError, OSError), legacy_xml_file_interface.write, filename, document)

    def test_read_empty_path(self):
        self.assertRaises(FileNotFoundError, legacy_xml_file_interface.read, '')

    def test_write_empty_path(self):
        document = {'Disco': 7}
        self.assertRaises(FileNotFoundError, legacy_xml_file_interface.write, '', document)

    def test_read_file_with_root_tag_only(self):
        document = legacy_xml_file_interface.read(self.get_static_file('test_read_file_with_root_tag_only.xml'))
        self.assertEqual(document, '', 'Document should have resolve to no file contents')

    def test_read_empty_file(self):
        # An empty XML file is the same as an invalidly formatted file
        self.assertRaises(xml.parsers.expat.ExpatError, legacy_xml_file_interface.read,
                          self.get_static_file('test_read_empty_file.xml'))

    def test_write_empty_file(self):
        document = {}
        filename = self.get_temp_file('test_write_empty_file.xml')
        legacy_xml_file_interface.write(filename, document)
        # Mainly testing for file contents, ignoring other details like encoding and line endings
        self.assertEqual(legacy_xml_file_interface.read(filename),
                         legacy_xml_file_interface.read(self.get_static_file('test_write_empty_file.xml')),
                         'Files do not match')

    def test_read_invalid_formatted_file(self):
        self.assertRaises(xml.parsers.expat.ExpatError, legacy_xml_file_interface.read,
                          self.get_static_file('test_read_invalid_formatted_file.xml'))

    def test_read_with_empty_tag(self):
        # An empty tag is not only invalid XML, but is also reserved for special use within the file interface
        self.assertRaises(xml.parsers.expat.ExpatError, legacy_xml_file_interface.read,
                          self.get_static_file('test_read_with_empty_tag.xml'))

    def test_read_and_rewrite_file(self):
        filename = 'test_read_and_rewrite_file.xml'
        document1 = legacy_xml_file_interface.read(self.get_static_file(filename))
        legacy_xml_file_interface.write(self.get_temp_file(filename), document1)
        document2 = legacy_xml_file_interface.read(self.get_temp_file(filename))
        self.assertEqual(document1, document2, 'Files do not match')

    def test_read_with_trailing_whitespace(self):
        filename = 'test_read_with_trailing_whitespace.xml'
        document = legacy_xml_file_interface.read(self.get_static_file(filename))
        self.assertEqual(document['Disco']['Beatdown'], '1 ', 'First entry is incorrect')
        self.assertEqual(document['Disco']['Elysium'], '2\n', 'Second entry is incorrect')

    def test_read_with_trailing_space_placeholder_in_key(self):
        filename = 'test_read_with_trailing_space_placeholder_in_key.xml'
        document = legacy_xml_file_interface.read(self.get_static_file(filename))
        self.assertEqual(document['Disco']['Beatdown'], '1', 'First entry is incorrect')
        self.assertEqual(document['Disco']['2'], 'Elysium', 'Second entry is incorrect')

    def test_read_with_empty_contents_in_tags(self):
        filename = 'test_read_with_empty_contents_in_tags.xml'
        document = legacy_xml_file_interface.read(self.get_static_file(filename))
        self.assertEqual(document['Disco']['Beatdown'], '', 'First entry is not empty')


if __name__ == "__main__":
    unittest.main()
