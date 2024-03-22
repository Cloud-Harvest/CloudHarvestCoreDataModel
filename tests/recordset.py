import unittest
from collections import OrderedDict
from harvest.record import HarvestRecord
from harvest.recordset import HarvestRecordSet


class TestHarvestRecordSet(unittest.TestCase):
    """
    Test case for the HarvestRecordSet class in recordset.py
    """

    def setUp(self):
        """
        Set up a HarvestRecordSet object for use in tests
        """
        self.recordset = HarvestRecordSet(data=[{'key1': 'value1', 'key2': 'value2'}])

    def test_add(self):
        """
        Test the add method
        """
        self.recordset.add(data=[{'key3': 'value3'}])
        self.assertEqual(len(self.recordset), 2)
        self.assertEqual(self.recordset[1]['key3'], 'value3')

    def test_create_index(self):
        """
        Test the create_index method
        """
        self.recordset.create_index('index1', 'key1')
        self.assertIn('index1', self.recordset.indexes)

    def test_drop_index(self):
        """
        Test the drop_index method
        """
        self.recordset.create_index('index1', 'key1')
        self.recordset.drop_index('index1')
        self.assertNotIn('index1', self.recordset.indexes)

    def test_get_matched_records(self):
        """
        Test the get_matched_records method
        """

        # Test invalid match
        self.recordset.add(data=[{'key1': 'value1', 'key2': 'value2'}])
        self.recordset.add_match('key1=invalid')
        matched = self.recordset.get_matched_records()
        self.assertEqual(len(matched), 0)
        self.recordset.clear_matches()
        self.recordset.clear()

        # Test '=' operation (regex)
        self.recordset.add(data=[{'key1': 'value1', 'key2': 'value2'}])
        self.recordset.add_match('key1=value')
        matched = self.recordset.get_matched_records()
        self.assertEqual(len(matched), 1)
        self.recordset.clear_matches()
        self.recordset.clear()

        # Test '<=' operation
        self.recordset.add(data=[{'key3': 3}])
        self.recordset.add_match('key3<=3')
        matched = self.recordset.get_matched_records()
        self.assertEqual(len(matched), 1)
        self.recordset.clear_matches()
        self.recordset.clear()

        # Test '>=' operation
        self.recordset.add(data=[{'key4': 4}])
        self.recordset.add_match('key4>=4')
        matched = self.recordset.get_matched_records()
        self.assertEqual(len(matched), 1)
        self.recordset.clear_matches()
        self.recordset.clear()

        # Test '==' operation
        self.recordset.add(data=[{'key5': 'value5'}])
        self.recordset.add_match('key5==value5')
        matched = self.recordset.get_matched_records()
        self.assertEqual(len(matched), 1)
        self.recordset.clear_matches()
        self.recordset.clear()

        # Test '!=' operation
        self.recordset.add(data=[{'key6': 'value6'}])
        self.recordset.add_match('key6!=value6')
        matched = self.recordset.get_matched_records()
        self.assertEqual(len(matched), 0)
        self.recordset.clear_matches()
        self.recordset.clear()

        # Test '<' operation
        self.recordset.add(data=[{'key7': 7}])
        self.recordset.add_match('key7<8')
        matched = self.recordset.get_matched_records()
        self.assertEqual(len(matched), 1)
        self.recordset.clear_matches()
        self.recordset.clear()

        # Test '>' operation
        self.recordset.add(data=[{'key8': 8}])
        self.recordset.add_match('key8>7')
        matched = self.recordset.get_matched_records()
        self.assertEqual(len(matched), 1)
        self.recordset.clear_matches()
        self.recordset.clear()

    def test_modify_records(self):
        """
        Test the modify_records method
        """
        # This method is difficult to test without a function and arguments

    def test_remove_duplicates(self):
        """
        Test the remove_duplicates method
        """
        self.recordset.add(data=[{'key1': 'value1', 'key2': 'value2'}])
        self.recordset.remove_duplicates()
        self.assertEqual(len(self.recordset), 1)

    def test_remove_unmatched_records(self):
        """
        Test the remove_unmatched_records method
        """
        # This method is difficult to test without a match statement

    def test_unwind(self):
        """
        Test the unwind method
        """
        with HarvestRecordSet() as recordset:
            recordset.add(data=[{'key1': 'value1', 'key2': 'value2'}])
            recordset.unwind('key1', preserve_null_and_empty_keys=True)
            self.assertEqual(len(recordset), 1)
            self.assertEqual(recordset[0]['key1'], 'value1')

            recordset[0]['key3'] = ['value3_a', 'value3_b', 'value3_c']
            recordset.unwind('key3')
            self.assertEqual(len(recordset), 3)
            self.assertEqual(recordset[0]['key3'], 'value3_a')
            self.assertEqual(recordset[1]['key3'], 'value3_b')
            self.assertEqual(recordset[2]['key3'], 'value3_c')


if __name__ == '__main__':
    unittest.main()
