import unittest
import sys
import filecmp
sys.path.append('../')
from meaningless import toml_file_interface


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    @staticmethod
    def get_static_file(filename):
        return f'./static/unit_tests_toml_file_interface/{filename}'

    @staticmethod
    def get_temp_file(filename):
        return f'./tmp/unit_tests_toml_file_interface/{filename}'

    def test_read(self):
        document = toml_file_interface.read(self.get_static_file('test_read.toml'))
        self.assertEqual(list(document.keys()), ['Disco'], 'Main keys are incorrect')
        self.assertEqual(document['Disco']['1'], 'Beatdown', 'First entry is incorrect')
        self.assertEqual(document['Disco']['2'], 'Elysium', 'Second entry is incorrect')

    def test_write(self):
        document = {'Disco': {'1': 'Beatdown', '2': 'Elysium'}}
        toml_file_interface.write(self.get_temp_file('test_write.toml'), document)
        # Mainly testing for file contents, ignoring other details like encoding and line endings
        self.assertEqual(toml_file_interface.read(self.get_static_file('test_write.toml')),
                         toml_file_interface.read(self.get_temp_file('test_write.toml')), 'Files do not match')

    def test_read_nonexistent_file(self):
        self.assertRaises(FileNotFoundError, toml_file_interface.read,
                          self.get_static_file('test_read_nonexistent_file.toml'))

    def test_write_overwrite(self):
        document = {'Disco': {'1': 'Beatdown', '2': 'Elysium'}}
        toml_file_interface.write(self.get_temp_file('test_write_overwrite.toml'), document)
        self.assertEqual(len(document['Disco']), 2, 'Number of entries is incorrect')
        document['Disco']['3'] = 'Fever'
        toml_file_interface.write(self.get_temp_file('test_write_overwrite.toml'), document)
        self.assertEqual(document['Disco']['3'], 'Fever', 'Third entry is incorrect')

    def test_write_string_contents(self):
        document = 'Ugh'
        file_path = self.get_temp_file('test_write_string_contents.toml')
        toml_file_interface.write(file_path, document)
        # String gets converted to a simple TOML structure
        expected = toml_file_interface.read(self.get_static_file('test_write_string_contents.toml'))
        actual = toml_file_interface.read(file_path)
        self.assertEqual(expected, actual, 'Files do not match')

    def test_write_list_contents(self):
        document = ['Disco', 'Fever']
        file_path = self.get_temp_file('test_write_list_contents.toml')
        toml_file_interface.write(file_path, document)
        # A list gets converted to a simple TOML structure
        expected = toml_file_interface.read(self.get_static_file('test_write_list_contents.toml'))
        actual = toml_file_interface.read(file_path)
        self.assertEqual(expected, actual, 'Files do not match')

    def test_read_path_exceeds_windows_limit(self):
        filename = 'G' * 255
        self.assertRaises((FileNotFoundError, OSError), toml_file_interface.read,
                          self.get_static_file(f'{filename}.toml'))

    def test_write_path_exceeds_windows_limit(self):
        document = {'Disco': 7}
        filename = 'G' * 255
        self.assertRaises((FileNotFoundError, OSError), toml_file_interface.write, f'./tmp/{filename}.toml',
                          document)

    def test_read_empty_path(self):
        self.assertRaises(FileNotFoundError, toml_file_interface.read, '')

    def test_write_empty_path(self):
        document = {'Disco': 7}
        self.assertRaises(FileNotFoundError, toml_file_interface.write, '', document)

    def test_read_empty_file(self):
        # An empty TOML file returns an empty dict (valid but empty TOML)
        result = toml_file_interface.read(self.get_static_file('test_read_empty_file.toml'))
        self.assertEqual(result, {}, 'Empty file should return empty dict')

    def test_write_empty_file(self):
        document = {}
        file_path = self.get_temp_file('test_write_empty_file.toml')
        toml_file_interface.write(file_path, document)
        self.assertTrue(filecmp.cmp(file_path, self.get_static_file('test_write_empty_file.toml')),
                        'Files do not match')

    def test_read_invalid_formatted_file(self):
        self.assertRaises(Exception, toml_file_interface.read,
                          self.get_static_file('test_read_invalid_formatted_file.toml'))


if __name__ == "__main__":
    unittest.main()