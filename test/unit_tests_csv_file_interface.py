import unittest
import sys
sys.path.append('../')
from meaningless import csv_file_interface


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    @staticmethod
    def get_static_file(filename):
        return f'./static/unit_tests_csv_file_interface/{filename}'

    @staticmethod
    def get_temp_file(filename):
        return f'./tmp/unit_tests_csv_file_interface/{filename}'

    def test_read(self):
        document = csv_file_interface.read(self.get_static_file('test_read.csv'))
        self.assertEqual(document['Disco']['42']['7'], 'Beatdown', 'Text is incorrect')
        self.assertEqual(len(document['Info'].keys()), 4, 'Number of informational items is incorrect')
        self.assertEqual(document['Info']['Language'], 'English', 'Language is incorrect')
        self.assertEqual(document['Info']['Translation'], 'Elysium', 'Translation is incorrect')

    def test_write(self):
        document = {'Disco': {1: {1: 'Beatdown', 2: 'Elysium'}},
                    'Info': {'Language': 'English', 'Translation': 'Fever'}}
        filename = 'test_write.csv'
        csv_file_interface.write(self.get_temp_file(filename), document)
        # Mainly testing for file contents, ignoring other details like encoding and line endings
        self.assertEqual(csv_file_interface.read(self.get_static_file(filename)),
                         csv_file_interface.read(self.get_temp_file(filename)), 'Files do not match')

    def test_read_nonexistent_file(self):
        self.assertRaises(FileNotFoundError, csv_file_interface.read,
                          self.get_static_file('test_read_nonexistent_file.csv'))

    def test_write_overwrite(self):
        document = {'Disco': {1: {1: 'Beatdown', 2: 'Elysium'}},
                    'Info': {'Language': 'English', 'Translation': 'Fever'}}
        filename = 'test_write_overwrite.csv'
        csv_file_interface.write(self.get_temp_file(filename), document)
        self.assertEqual(len(document['Disco'][1]), 2, 'Number of entries is incorrect')
        document['Disco'][1][3] = 'Ball'
        csv_file_interface.write(self.get_temp_file(filename), document)
        self.assertEqual(document['Disco'][1][3], 'Ball', 'Third entry is incorrect')

    def test_read_with_header_only(self):
        self.assertEqual(csv_file_interface.read(self.get_static_file('test_read_with_header_only.csv')), {},
                         'Header-only file did not return an empty object')

    def test_read_with_insufficient_columns(self):
        document = csv_file_interface.read(self.get_static_file('test_read_with_insufficient_columns.csv'))
        self.assertIsNone(document['Info']['Translation'], 'Translation is not empty')

    def test_read_with_single_column(self):
        document = csv_file_interface.read(self.get_static_file('test_read_with_single_column.csv'))
        self.assertIsNone(document['Info']['Translation'], 'Translation is not empty')
        self.assertIsNone(document['Info']['Language'], 'Language is not empty')
        self.assertIsNone(document['Disco'][None][None], 'Text is not empty')

    def test_write_with_multiple_books(self):
        document = {'Disco': {1: {1: 'Beatdown', 2: 'Elysium'}},
                    'Ball': {1: {1: 'Beatdown', 2: 'Elysium'}},
                    'Info': {'Language': 'English', 'Translation': 'Fever'}}
        filename = 'test_write_with_multiple_books.csv'
        csv_file_interface.write(self.get_temp_file(filename), document)
        self.assertEqual(csv_file_interface.read(self.get_static_file(filename)),
                         csv_file_interface.read(self.get_temp_file(filename)), 'Files do not match')

    def test_write_with_passage_as_list(self):
        document = {'Disco': {1: {1: ['Beatdown', 'Elysium']}},
                    'Info': {'Language': 'English', 'Translation': 'Fever'}}
        filename = 'test_write_with_passage_as_list.csv'
        csv_file_interface.write(self.get_temp_file(filename), document)
        # List gets converted into its string representation
        self.assertEqual(csv_file_interface.read(self.get_static_file(filename)),
                         csv_file_interface.read(self.get_temp_file(filename)), 'Files do not match')

    def test_write_without_info(self):
        document = {'Disco': {1: {1: 'Beatdown', 2: 'Elysium'}}}
        filename = 'test_write_without_info.csv'
        # Refuse to write the file without the associated metadata
        self.assertRaises(KeyError, csv_file_interface.write, self.get_temp_file(filename), document)

    def test_write_without_contents(self):
        document = {'Info': {'Language': 'English', 'Translation': 'Fever'}}
        filename = 'test_write_without_contents.csv'
        csv_file_interface.write(self.get_temp_file(filename), document)
        # Do not expect metadata to be written to the file, as there is no data to correlate it with
        self.assertEqual(csv_file_interface.read(self.get_static_file(filename)),
                         csv_file_interface.read(self.get_temp_file(filename)), 'Files do not match')

    def test_write_with_empty_info_items(self):
        document = {'Disco': {1: {1: 'Beatdown', 2: 'Elysium'}}, 'Info': {'Language': None, 'Translation': None}}
        filename = 'test_write_with_empty_info_items.csv'
        csv_file_interface.write(self.get_temp_file(filename), document)
        # Metadata is still technically present, but deliberately set as empty
        self.assertEqual(csv_file_interface.read(self.get_static_file(filename)),
                         csv_file_interface.read(self.get_temp_file(filename)), 'Files do not match')

    def test_write_with_empty_book(self):
        document = {'Disco': {}, 'Info': {'Language': 'English', 'Translation': 'Fever'}}
        filename = 'test_write_with_empty_book.csv'
        csv_file_interface.write(self.get_temp_file(filename), document)
        self.assertEqual(csv_file_interface.read(self.get_static_file(filename)),
                         csv_file_interface.read(self.get_temp_file(filename)), 'Files do not match')

    def test_write_with_empty_chapter(self):
        document = {'Disco': {None: 'Elysium'}, 'Info': {'Language': 'English', 'Translation': 'Fever'}}
        filename = 'test_write_with_empty_book.csv'
        self.assertRaises(TypeError, csv_file_interface.write, self.get_temp_file(filename), document)

    def test_write_with_empty_passage(self):
        document = {'Disco': {1: None}, 'Info': {'Language': 'English', 'Translation': 'Fever'}}
        filename = 'test_write_with_empty_passage.csv'
        self.assertRaises(TypeError, csv_file_interface.write, self.get_temp_file(filename), document)

    def test_write_string_contents(self):
        document = 'Ugh'
        # Writing should cause an error, since it relies on explicitly defined dictionary keys
        self.assertRaises(TypeError, csv_file_interface.write, document)

    def test_write_list_contents(self):
        document = ['Disco', 'Fever']
        # Writing should cause an error, since it relies on explicitly defined dictionary keys
        self.assertRaises(TypeError, csv_file_interface.write, document)

    def test_read_path_exceeds_windows_limit(self):
        filename = 'G' * 255
        self.assertRaises((FileNotFoundError, OSError), csv_file_interface.read,
                          self.get_static_file(f'{filename}.csv'))

    def test_write_path_exceeds_windows_limit(self):
        document = {'Disco': 7}
        filename = 'G' * 255
        self.assertRaises((FileNotFoundError, OSError), csv_file_interface.write, f'./tmp/{filename}.csv', document)

    def test_read_empty_path(self):
        self.assertRaises(FileNotFoundError, csv_file_interface.read, '')

    def test_write_empty_path(self):
        document = {'Disco': 7}
        self.assertRaises(FileNotFoundError, csv_file_interface.write, '', document)

    def test_read_empty_file(self):
        filename = 'test_read_empty_file.csv'
        # An empty CSV file can't be processed, since a header row is assumed to exist
        self.assertRaises(StopIteration, csv_file_interface.read, self.get_static_file(filename))

    def test_write_empty_file(self):
        document = {}
        filename = 'test_write_empty_file.csv'
        # Empty document still contains no metadata, which should trigger an exception
        self.assertRaises(KeyError, csv_file_interface.write, self.get_temp_file(filename), document)


if __name__ == "__main__":
    unittest.main()
