import unittest
import sys
from ruamel.yaml.parser import ParserError
sys.path.append('../')
from meaningless import yaml_file_interface


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def get_static_file(self, filename):
        return './static/unit_tests_yaml_file_interface/{0}'.format(filename)

    def test_read(self):
        document = yaml_file_interface.read(self.get_static_file('test_read.yaml'))
        self.assertEqual(list(document.keys()), ['Disco'], 'Main keys are incorrect')
        self.assertEqual(document['Disco'][1], 'Beatdown', 'First entry is incorrect')
        self.assertEqual(document['Disco'][2], 'Elysium', 'Second entry is incorrect')

    def test_write(self):
        document = {'Disco': {1: 'Beatdown', 2: 'Elysium'}}
        yaml_file_interface.write('./tmp/test_write.yaml', document)
        self.assertEqual(yaml_file_interface.read('./tmp/test_write.yaml'),
                         yaml_file_interface.read(self.get_static_file('test_write.yaml')),
                         'Files do not match')

    def test_read_nonexistent_file(self):
        self.assertRaises(FileNotFoundError, yaml_file_interface.read,
                          self.get_static_file('test_read_nonexistent_file.yaml'))

    def test_write_overwrite(self):
        document = {'Disco': {1: 'Beatdown', 2: 'Elysium'}}
        yaml_file_interface.write('./tmp/test_write_overwrite.yaml', document)
        self.assertEqual(len(document['Disco']), 2, 'Number of entries is incorrect')
        document['Disco'][3] = 'Fever'
        yaml_file_interface.write('./tmp/test_write_overwrite.yaml', document)
        self.assertEqual(document['Disco'][3], 'Fever', 'Third entry is incorrect')

    def test_write_string_contents(self):
        document = 'Ugh'
        yaml_path = './tmp/test_write_string_contents.yaml'
        yaml_file_interface.write(yaml_path, document)
        # Despite not being a dictionary, this writes valid YAML to the file - the result being a single YAML key
        self.assertEqual(yaml_file_interface.read(yaml_path),
                         yaml_file_interface.read(self.get_static_file('test_write_string_contents.yaml')),
                         'Files do not match')

    def test_write_list_contents(self):
        document = ['Disco', 'Fever']
        yaml_path = './tmp/test_write_list_contents.yaml'
        yaml_file_interface.write(yaml_path, document)
        # A list should just translate to a linear series of YAML keys
        self.assertEqual(yaml_file_interface.read(yaml_path),
                         yaml_file_interface.read(self.get_static_file('test_write_list_contents.yaml')),
                         'Files do not match')

    def test_read_path_exceeds_windows_limit(self):
        filename = 'G' * 255
        self.assertRaises((FileNotFoundError, OSError), yaml_file_interface.read,
                          self.get_static_file('{0}.yaml'.format(filename)))

    def test_write_path_exceeds_windows_limit(self):
        document = {'Disco': 7}
        filename = 'G' * 255
        self.assertRaises((FileNotFoundError, OSError), yaml_file_interface.write, './tmp/{0}.yaml'.format(filename),
                          document)

    def test_read_empty_path(self):
        self.assertRaises(FileNotFoundError, yaml_file_interface.read, '')

    def test_write_empty_path(self):
        document = {'Disco': 7}
        self.assertRaises(FileNotFoundError, yaml_file_interface.write, '', document)

    def test_read_empty_file(self):
        document = yaml_file_interface.read(self.get_static_file('test_read_empty_file.yaml'))
        self.assertEqual(document, None, 'Empty file was not handled correctly')

    def test_write_empty_file(self):
        document = {}
        yaml_path = './tmp/test_write_empty_file.yaml'
        yaml_file_interface.write(yaml_path, document)
        self.assertEqual(yaml_file_interface.read(yaml_path),
                         yaml_file_interface.read(self.get_static_file('test_write_empty_file.yaml')),
                         'Files do not match')

    def test_read_invalid_formatted_file(self):
        self.assertRaises(ParserError, yaml_file_interface.read,
                          self.get_static_file('test_read_invalid_formatted_file.yaml'))


if __name__ == "__main__":
    unittest.main()
