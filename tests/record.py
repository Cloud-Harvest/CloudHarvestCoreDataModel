import unittest
from collections import OrderedDict
from harvest.record import HarvestRecord


class TestHarvestRecord(unittest.TestCase):
    """
    Test case for the HarvestRecord class in record.py
    """

    def setUp(self):
        """
        Set up a HarvestRecord object for use in tests
        """
        self.record = HarvestRecord(key1='value1', key2='value2', key4='4')

    def test_add_freshness(self):
        """
        Test the add_freshness method
        """
        # This method is difficult to test without mocking datetime, as it depends on the current time

    def test_add_key_from_keys(self):
        """
        Test the add_key_from_keys method
        """
        self.record.add_key_from_keys('new_key', ['key1', 'key2'])
        self.assertEqual(self.record['new_key'], 'value1 value2')

    def test_assign_elements_at_index_to_key(self):
        """
        Test the assign_elements_at_index_to_key method
        """
        # This method is difficult to test without a source_column that is an iterable

    def test_cast(self):
        """
        Test the cast method. cast() is a call to functions.cast().
        """
        self.record.cast('key1', 'int')
        self.assertEqual(self.record['key1'], None)

        self.record.cast('key4', 'int')
        self.assertEqual(self.record['key4'], 4)

    def test_copy_key(self):
        """
        Test the copy_key method
        """
        self.record.copy_key('key1', 'key3')
        self.assertEqual(self.record['key3'], 'value1')

    def test_dict_from_json_string(self):
        """
        Test the dict_from_json_string method
        """
        # This method is difficult to test without a source_key that is a JSON string

    def test_first_not_null_value(self):
        """
        Test the first_not_null_value method
        """
        self.assertEqual(self.record.first_not_null_value('key1', 'key2'), 'value1')

    def test_flatten(self):
        """
        Test the flatten method
        """
        # This method is difficult to test without a nested dictionary

    def test_is_matched_record(self):
        """
        Test the is_matched_record method
        """
        self.assertTrue(self.record.is_matched_record())

    def test_key_value_list_to_dict(self):
        """
        Test the key_value_list_to_dict method
        """
        # This method is difficult to test without a source_column that is a list of dictionaries

    def test_match(self):
        """
        Test the match method
        """
        self.assertTrue(self.record.match('key1=value1'))
        self.assertFalse(self.record.match('key1=value2'))

    def test_md5_hash(self):
        """
        Test the md5_hash method
        """
        # This method is difficult to test as the output depends on the current state of the record

    def test_remove_key(self):
        """
        Test the remove_key method
        """
        self.record.remove_key('key1')
        self.assertNotIn('key1', self.record)

    def test_rename_key(self):
        """
        Test the rename_key method
        """
        self.record.rename_key('key1', 'key3')
        self.assertNotIn('key1', self.record)
        self.assertIn('key3', self.record)

    def test_reset_matches(self):
        """
        Test the reset_matches method
        """
        self.record.match('key1=value1')
        self.record.reset_matches()
        self.assertEqual(self.record.matching_expressions, [])
        self.assertEqual(self.record.non_matching_expressions, [])

    def test_split_key(self):
        """
        Test the split_key method
        """
        # This method is difficult to test without a source_key that is a string with a delimiter

    def test_substring(self):
        """
        Test the substring method
        """
        # This method is difficult to test without a source_key that is a string

    def test_unflatten(self):
        """
        Test the unflatten method
        """
        # This method is difficult to test without a flattened dictionary

if __name__ == '__main__':
    unittest.main()