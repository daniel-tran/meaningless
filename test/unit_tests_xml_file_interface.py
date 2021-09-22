import unittest
import sys
import xml
sys.path.append('../')
from meaningless import xml_file_interface


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    @staticmethod
    def get_static_file(filename):
        return './static/unit_tests_xml_file_interface/{0}'.format(filename)

    @staticmethod
    def get_temp_file(filename):
        return './tmp/unit_tests_xml_file_interface/{0}'.format(filename)

    def test_read(self):
        document = xml_file_interface.read(self.get_static_file('test_read.xml'))
        self.assertEqual(list(document.keys()), ['Disco'], 'Main keys are incorrect')
        self.assertEqual(document['Disco']['Beatdown'], '1', 'First entry is incorrect')
        self.assertEqual(document['Disco']['Elysium'], '2', 'Second entry is incorrect')

    def test_write(self):
        document = {'Disco': {'1': 'Beatdown', '2': 'Elysium'}}
        filename = 'test_write.xml'
        xml_file_interface.write(self.get_temp_file(filename), document)
        # Mainly testing for file contents, ignoring other details like encoding and line endings
        self.assertEqual(xml_file_interface.read(self.get_static_file(filename)),
                         xml_file_interface.read(self.get_temp_file(filename)), 'Files do not match')

    def test_write_overwrite(self):
        filename = 'test_write_overwrite.xml'
        document = {'Disco': {'1': 'Beatdown', '2': 'Elysium'}}
        xml_file_interface.write(self.get_temp_file(filename), document)
        document['Disco']['3'] = 'Fever'
        xml_file_interface.write(self.get_temp_file(filename), document)
        # Assert that the file has been modified according to the latest changes
        modified_document = xml_file_interface.read(self.get_temp_file(filename))
        self.assertEqual(len(modified_document['Disco']), 3, 'Number of entries is incorrect')
        self.assertEqual(modified_document['Disco']['3'], 'Fever', 'Third entry is incorrect')

    def test_read_with_space_placeholders_in_top_level_key(self):
        document = xml_file_interface.read(
            self.get_static_file('test_read_with_space_placeholders_in_top_level_key.xml'))
        self.assertEqual(list(document.keys()), ['Disc o'], 'Main keys are incorrect')
        self.assertEqual(document['Disc o']['Beatdown'], '1', 'First entry is incorrect')
        self.assertEqual(document['Disc o']['Elysium'], '2', 'Second entry is incorrect')

    def test_write_with_spaces_in_top_level_key(self):
        document = {'Disc o': {'Beatdown': '1', 'Elysium': '2'}}
        filename = 'test_write_with_spaces_in_top_level_key.xml'
        xml_file_interface.write(self.get_temp_file(filename), document)
        # Mainly testing for file contents, ignoring other details like encoding and line endings
        self.assertEqual(xml_file_interface.read(self.get_static_file(filename)),
                         xml_file_interface.read(self.get_temp_file(filename)), 'Files do not match')

    def test_read_with_number_prefixed_top_level_key(self):
        document = xml_file_interface.read(self.get_static_file('test_read_with_number_prefixed_top_level_key.xml'))
        self.assertEqual(list(document.keys()), ['1 Disco'], 'Main keys are incorrect')
        self.assertEqual(document['1 Disco']['Beatdown'], '1', 'First entry is incorrect')
        self.assertEqual(document['1 Disco']['Elysium'], '2', 'Second entry is incorrect')

    def test_write_with_number_prefixed_top_level_key(self):
        document = {'1 Disco': {'Beatdown': '1', 'Elysium': '2'}}
        filename = 'test_write_with_number_prefixed_top_level_key.xml'
        xml_file_interface.write(self.get_temp_file(filename), document)
        # Mainly testing for file contents, ignoring other details like encoding and line endings
        self.assertEqual(xml_file_interface.read(self.get_static_file(filename)),
                         xml_file_interface.read(self.get_temp_file(filename)), 'Files do not match')

    def test_write_with_number_top_level_key(self):
        filename = 'test_write_with_number_top_level_key.xml'
        document = {1: {'Beatdown': 1, 'Elysium': 2}}
        xml_file_interface.write(self.get_temp_file(filename), document)
        result = xml_file_interface.read(self.get_temp_file(filename))
        self.assertEqual(result[1]['Beatdown'], '1', 'First entry is incorrect')
        self.assertEqual(result[1]['Elysium'], '2', 'Second entry is incorrect')

    def test_read_with_number_prefixed_second_level_key(self):
        filename = 'test_read_with_number_prefixed_second_level_key.xml'
        document = xml_file_interface.read(self.get_static_file(filename))
        self.assertEqual(document['Disco']['1'], 'Beatdown', 'First entry is incorrect')
        self.assertEqual(document['Disco']['2'], 'Elysium', 'Second entry is incorrect')

    def test_read_nonexistent_file(self):
        self.assertRaises(FileNotFoundError, xml_file_interface.read,
                          self.get_static_file('test_read_nonexistent_file.xml'))

    def test_write_string_contents(self):
        document = 'Ugh'
        filename = self.get_temp_file('test_write_string_contents.xml')
        # XML file interface only supports data structures with keys
        self.assertRaises(AttributeError, xml_file_interface.write, filename, document)

    def test_write_list_contents(self):
        document = ['Disco', 'Fever']
        filename = self.get_temp_file('test_write_list_contents.xml')
        # XML file interface only supports data structures with keys
        self.assertRaises(AttributeError, xml_file_interface.write, filename, document)

    def test_read_path_exceeds_windows_limit(self):
        filename = '{0}.xml'.format('G' * 255)
        self.assertRaises((FileNotFoundError, OSError), xml_file_interface.read,
                          self.get_static_file(filename))

    def test_write_path_exceeds_windows_limit(self):
        document = {'Disco': 7}
        filename = './tmp/{0}.xml'.format('G' * 255)
        self.assertRaises((FileNotFoundError, OSError), xml_file_interface.write, filename, document)

    def test_read_empty_path(self):
        self.assertRaises(FileNotFoundError, xml_file_interface.read, '')

    def test_write_empty_path(self):
        document = {'Disco': 7}
        self.assertRaises(FileNotFoundError, xml_file_interface.write, '', document)

    def test_read_file_with_root_tag_only(self):
        document = xml_file_interface.read(self.get_static_file('test_read_file_with_root_tag_only.xml'))
        self.assertIsNone(document, 'Document should not have additional content')

    def test_read_empty_file(self):
        # An empty XML file is the same as an invalidly formatted file
        self.assertRaises(xml.parsers.expat.ExpatError, xml_file_interface.read,
                          self.get_static_file('test_read_empty_file.xml'))

    def test_write_empty_file(self):
        document = {}
        filename = self.get_temp_file('test_write_empty_file.xml')
        xml_file_interface.write(filename, document)
        # Mainly testing for file contents, ignoring other details like encoding and line endings
        self.assertEqual(xml_file_interface.read(filename),
                         xml_file_interface.read(self.get_static_file('test_write_empty_file.xml')),
                         'Files do not match')

    def test_read_invalid_formatted_file(self):
        self.assertRaises(xml.parsers.expat.ExpatError, xml_file_interface.read,
                          self.get_static_file('test_read_invalid_formatted_file.xml'))

    def test_read_with_empty_tag(self):
        # An empty tag is not only invalid XML, but is also reserved for special use within the file interface
        self.assertRaises(xml.parsers.expat.ExpatError, xml_file_interface.read,
                          self.get_static_file('test_read_with_empty_tag.xml'))

    def test_read_and_rewrite_file(self):
        filename = 'test_read_and_rewrite_file.xml'
        document1 = xml_file_interface.read(self.get_static_file(filename))
        xml_file_interface.write(self.get_temp_file(filename), document1)
        document2 = xml_file_interface.read(self.get_temp_file(filename))
        self.assertEqual(document1, document2, 'Files do not match')

    def test_read_with_trailing_whitespace(self):
        filename = 'test_read_with_trailing_whitespace.xml'
        document = xml_file_interface.read(self.get_static_file(filename))
        self.assertEqual(document['Disco']['Beatdown'], '1 ', 'First entry is incorrect')
        self.assertEqual(document['Disco']['Elysium'], '2\n', 'Second entry is incorrect')


if __name__ == "__main__":
    unittest.main()
