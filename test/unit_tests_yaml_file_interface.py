import unittest
import sys
import os
import filecmp
sys.path.append('../src/')
from meaningless.utilities import yaml_file_interface


class UnitTests(unittest.TestCase):

    # Note: Tests will only be run if they are prefixed with test_ in their method name.
    #       All other methods will simply be interpreted as test helper functions.

    def test_read(self):
        document = yaml_file_interface.read('./static/test_read.yaml')
        self.assertEqual(list(document.keys()), ['Disco'], 'Main keys are incorrect')
        self.assertEqual(document['Disco'][1], 'Beatdown', 'First entry is incorrect')
        self.assertEqual(document['Disco'][2], 'Elysium', 'Second entry is incorrect')

    def test_write(self):
        document = {'Disco': {1: 'Beatdown', 2: 'Elysium'}}
        yaml_file_interface.write('./tmp/test_write.yaml', document)
        self.assertTrue(filecmp.cmp('./tmp/test_write.yaml', './static/test_write.yaml'), 'Files do not match')

    def test_read_nonexistent_file(self):
        document = yaml_file_interface.read('./static/test_read_nonexistent_file.yaml')
        self.assertEqual(document, None, 'Non-existent file was not handled correctly')

    def test_write_overwrite(self):
        document = {'Disco': {1: 'Beatdown', 2: 'Elysium'}}
        yaml_file_interface.write('./tmp/test_write_overwrite.yaml', document)
        self.assertEqual(len(document['Disco']), 2, 'Number of entries is incorrect')
        document['Disco'][3] = 'Fever'
        yaml_file_interface.write('./tmp/test_write_overwrite.yaml', document)
        self.assertEqual(document['Disco'][3], 'Fever', 'Third entry is incorrect')

    def test_write_invalid_contents(self):
        document = 'Ugh'
        yaml_file_interface.write('./tmp/test_write_invalid_contents.yaml', document)
        self.assertFalse(os.path.exists('./tmp/test_write_invalid_contents.yaml'), 'File should not have been written')

    def test_read_path_exceeds_windows_limit(self):
        filename = 'G' * 255
        document = yaml_file_interface.read('./static/{0}.yaml'.format(filename))
        self.assertEqual(document, None, 'Non-existent file was not handled correctly')

    def test_write_path_exceeds_windows_limit(self):
        document = {'Disco': 7}
        filename = 'G' * 255
        yaml_file_interface.write('./tmp/{0}.yaml'.format(filename), document)
        self.assertFalse(os.path.exists('./tmp/{0}.yaml'.format(filename)), 'File should not have been written')

    def test_read_empty_path(self):
        document = yaml_file_interface.read('')
        self.assertEqual(document, None, 'Non-existent file was not handled correctly')

    def test_write_empty_path(self):
        document = {'Disco': 7}
        rc = yaml_file_interface.write('', document)
        self.assertEqual(rc, 0, 'File should not have been written')

    def test_read_empty_file(self):
        document = yaml_file_interface.read('./static/test_read_empty_file.yaml')
        self.assertEqual(document, None, 'Empty file was not handled correctly')

    def test_write_empty_file(self):
        document = {}
        yaml_file_interface.write('./tmp/test_write_empty_file.yaml', document)
        self.assertFalse(os.path.exists('./tmp/test_write_empty_file.yaml'), 'File should not have been written')

    def test_read_invalid_formatted_file(self):
        document = yaml_file_interface.read('./static/test_read_invalid_formatted_file.yaml')
        self.assertEqual(document, None, 'File was not handled correctly')

if __name__ == "__main__":
    unittest.main()
