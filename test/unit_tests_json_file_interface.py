import unittest
import sys
import filecmp
import json
sys.path.append('../')
from meaningless import json_file_interface


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    @staticmethod
    def get_static_file(filename):
        return './static/unit_tests_json_file_interface/{0}'.format(filename)

    @staticmethod
    def get_temp_file(filename):
        return './tmp/unit_tests_json_file_interface/{0}'.format(filename)

    def test_read(self):
        document = json_file_interface.read(self.get_static_file('test_read.json'))
        self.assertEqual(list(document.keys()), ['Disco'], 'Main keys are incorrect')
        self.assertEqual(document['Disco']['1'], 'Beatdown', 'First entry is incorrect')
        self.assertEqual(document['Disco']['2'], 'Elysium', 'Second entry is incorrect')

    def test_write(self):
        document = {'Disco': {1: 'Beatdown', 2: 'Elysium'}}
        json_file_interface.write(self.get_temp_file('test_write.json'), document)
        self.assertTrue(filecmp.cmp(self.get_temp_file('test_write.json'),
                                    self.get_static_file('test_write.json')), 'Files do not match')

    def test_read_nonexistent_file(self):
        self.assertRaises(FileNotFoundError, json_file_interface.read,
                          self.get_static_file('test_read_nonexistent_file.json'))

    def test_write_overwrite(self):
        document = {'Disco': {1: 'Beatdown', 2: 'Elysium'}}
        json_file_interface.write(self.get_temp_file('test_write_overwrite.json'), document)
        self.assertEqual(len(document['Disco']), 2, 'Number of entries is incorrect')
        document['Disco'][3] = 'Fever'
        json_file_interface.write(self.get_temp_file('test_write_overwrite.json'), document)
        self.assertEqual(document['Disco'][3], 'Fever', 'Third entry is incorrect')

    def test_write_string_contents(self):
        document = 'Ugh'
        file_path = self.get_temp_file('test_write_string_contents.json')
        json_file_interface.write(file_path, document)
        # Despite not being a dictionary, this writes valid YAML to the file - the result being a single YAML key
        self.assertTrue(filecmp.cmp(file_path, self.get_static_file('test_write_string_contents.json')),
                        'Files do not match')

    def test_write_list_contents(self):
        document = ['Disco', 'Fever']
        file_path = self.get_temp_file('test_write_list_contents.json')
        json_file_interface.write(file_path, document)
        # A list should just translate to a linear series of YAML keys
        self.assertTrue(filecmp.cmp(file_path, self.get_static_file('test_write_list_contents.json')),
                        'Files do not match')

    def test_read_path_exceeds_windows_limit(self):
        filename = 'G' * 255
        self.assertRaises(FileNotFoundError, json_file_interface.read,
                          self.get_static_file('{0}.json'.format(filename)))

    def test_write_path_exceeds_windows_limit(self):
        document = {'Disco': 7}
        filename = 'G' * 255
        self.assertRaises(FileNotFoundError, json_file_interface.write, './tmp/{0}.json'.format(filename), document)

    def test_read_empty_path(self):
        self.assertRaises(FileNotFoundError, json_file_interface.read, '')

    def test_write_empty_path(self):
        document = {'Disco': 7}
        self.assertRaises(FileNotFoundError, json_file_interface.write, '', document)

    def test_read_empty_file(self):
        # An empty JSON file is the same as an invalidly formatted file
        self.assertRaises(json.decoder.JSONDecodeError, json_file_interface.read,
                          self.get_static_file('test_read_empty_file.json'))

    def test_write_empty_file(self):
        document = {}
        file_path = self.get_temp_file('test_write_empty_file.json')
        json_file_interface.write(file_path, document)
        self.assertTrue(filecmp.cmp(file_path, self.get_static_file('test_write_empty_file.json')),
                        'Files do not match')

    def test_read_invalid_formatted_file(self):
        self.assertRaises(json.decoder.JSONDecodeError, json_file_interface.read,
                          self.get_static_file('test_read_invalid_formatted_file.json'))

if __name__ == "__main__":
    unittest.main()
