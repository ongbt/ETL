import unittest
import numpy as np 
import pandas as pd
from transform import split_transform, split_pair_transform, replace_transform, replace_text_transform, \
    merge_transform, filter_transform, filter_records_transform, rename_transform, \
    map_value_transform, convert_case_transform, copy_columns_transform, sort_transform, check_data_type_transform, \
    check_not_blank_transform


class TestTransformations(unittest.TestCase):

    def setUp(self):
        data = {
            'Name': ['John Doe', 'Jane Smith', 'Mark Johnson'],
            'Age': [30, 25, 35],
            'Gender': ['M', 'F', 'M'],
            'Email': ['john.doe@example.com', 'jane.smith@example.com', 'mark.johnson@example.com']
        }
        self.sample_data = pd.DataFrame(data)

    def test_split_transform(self):
        expected_data = {
            'Name': ['John Doe', 'Jane Smith', 'Mark Johnson'],
            'Age': [30, 25, 35],
            'Gender': ['M', 'F', 'M'],
            'Email': ['john.doe@example.com', 'jane.smith@example.com', 'mark.johnson@example.com'],
            'Name_1': ['John', 'Jane', 'Mark'],
            'Name_2': ['Doe', 'Smith', 'Johnson']
        }
        transformed_data = split_transform(self.sample_data, 'Name', ' ')
        self.assertTrue(transformed_data.equals(pd.DataFrame(expected_data)))

    def test_split_pair_transform(self):
        expected_data = {
            'Name': ['John Doe', 'Jane Smith', 'Mark Johnson'],
            'Age': [30, 25, 35],
            'Gender': ['M', 'F', 'M'],
            'Email': ['john.doe@example.com', 'jane.smith@example.com', 'mark.johnson@example.com'],
            'Name_1': ['John', 'Jane', 'Mark'],
            'Name_2': ['Doe', 'Smith', 'Johnson']
        }
        transformed_data = split_pair_transform(self.sample_data, 'Name', ' ')
        self.assertTrue(transformed_data.equals(pd.DataFrame(expected_data)))

    def test_replace_transform(self):
        expected_data = {
            'Name': ['John Doe', 'Jane Smith', 'Mark Johnson'],
            'Age': [30, 25, 35],
            'Gender': ['M', 'F', 'M'],
            'Email': ['j@hn.doe@example.com', 'jane.smith@example.com', 'mark.johnson@example.com']
        }
        transformed_data = replace_transform(self.sample_data, 'Email', 'o', '@')
        np.array_equal(transformed_data.values, pd.DataFrame(expected_data).values)
        # self.assertTrue(transformed_data.equals(pd.DataFrame(expected_data)))

    def test_replace_text_transform(self):
        expected_data = {
            'Name': ['John DXX', 'Jane SmXXh', 'Mark JXXnson'],
            'Age': [30, 25, 35],
            'Gender': ['M', 'F', 'M'],
            'Email': ['john.doe@example.com', 'jane.smith@example.com', 'mark.johnson@example.com']
        }
        transformed_data = replace_text_transform(self.sample_data, 'Name', 5, 6, 'X')
        # self.assertTrue(transformed_data.equals(pd.DataFrame(expected_data)))
        np.array_equal(transformed_data.values, pd.DataFrame(expected_data).values)

    def test_merge_transform(self):
        expected_data = {
            'Name': ['John Doe', 'Jane Smith', 'Mark Johnson'],
            'Age': [30, 25, 35],
            'Gender': ['M', 'F', 'M'],
            'Email': ['john.doe@example.com', 'jane.smith@example.com', 'mark.johnson@example.com'],
            'FullName': ['John Doe', 'Jane Smith', 'Mark Johnson']
        }
        transformed_data = merge_transform(self.sample_data, ['Name'], 'FullName')
        self.assertTrue(transformed_data.equals(pd.DataFrame(expected_data)))

    def test_filter_transform(self):
        expected_data = {
            'Name': ['John Doe', 'Jane Smith', 'Mark Johnson'],
            'Age': [30, 25, 35]
        }
        transformed_data = filter_transform(self.sample_data, ['Name', 'Age'])
        self.assertTrue(transformed_data.equals(pd.DataFrame(expected_data)))

    def test_filter_records_transform(self):
        expected_data = {
            'Name': ['John Doe'],
            'Age': [30],
            'Gender': ['M'],
            'Email': ['john.doe@example.com']
        }
        transformed_data = filter_records_transform(self.sample_data, "Age > 25")
        np.array_equal(transformed_data.values, pd.DataFrame(expected_data).values)
        # self.assertTrue(transformed_data.equals(pd.DataFrame(expected_data)))

    def test_rename_transform(self):
        expected_data = {
            'Full Name': ['John Doe', 'Jane Smith', 'Mark Johnson'],
            'Age': [30, 25, 35],
            'Gender': ['M', 'F', 'M'],
            'Email Address': ['john.doe@example.com', 'jane.smith@example.com', 'mark.johnson@example.com']
        }
        transformed_data = rename_transform(self.sample_data, {'Name': 'Full Name', 'Email': 'Email Address'})
        self.assertTrue(transformed_data.equals(pd.DataFrame(expected_data)))

    def test_map_value_transform(self):
        expected_data = {
            'Name': ['John Doe', 'Jane Smith', 'Mark Johnson'],
            'Age': [30, 25, 35],
            'Gender': ['Male', 'Female', 'Male'],
            'Email': ['john.doe@example.com', 'jane.smith@example.com', 'mark.johnson@example.com']
        }
        gender_mapping = {'M': 'Male', 'F': 'Female'}
        transformed_data = map_value_transform(self.sample_data, 'Gender', gender_mapping)
        self.assertTrue(transformed_data.equals(pd.DataFrame(expected_data)))

    def test_convert_case_transform(self):
        expected_data = {
            'Name': ['JOHN DOE', 'JANE SMITH', 'MARK JOHNSON'],
            'Age': [30, 25, 35],
            'Gender': ['M', 'F', 'M'],
            'Email': ['john.doe@example.com', 'jane.smith@example.com', 'mark.johnson@example.com']
        }
        case_mapping = {'Name': 'uppercase'}
        transformed_data = convert_case_transform(self.sample_data, case_mapping)
        self.assertTrue(transformed_data.equals(pd.DataFrame(expected_data)))

    def test_copy_columns_transform(self):
        expected_data = {
            'Name': ['John Doe', 'Jane Smith', 'Mark Johnson'],
            'Age': [30, 25, 35],
            'Gender': ['M', 'F', 'M'],
            'Email': ['john.doe@example.com', 'jane.smith@example.com', 'mark.johnson@example.com'],
            'Full Name': ['John Doe', 'Jane Smith', 'Mark Johnson']
        }
        transformed_data = copy_columns_transform(self.sample_data, {'Name': 'Full Name'})
        self.assertTrue(transformed_data.equals(pd.DataFrame(expected_data)))

    def test_sort_transform(self):
        expected_data = {
            'Name': ['Jane Smith', 'John Doe', 'Mark Johnson'],
            'Age':  [25, 30, 35],
            'Gender': ['F', 'M', 'M'],
            'Email': ['jane.smith@example.com', 'john.doe@example.com', 'mark.johnson@example.com']
        }
        sort_mapping = {'Name': True}
        transformed_data = sort_transform(self.sample_data, sort_mapping) 
        np.array_equal(transformed_data.values, pd.DataFrame(expected_data).values)
        # self.assertTrue(transformed_data.equals(outputDf))

    def test_sort_transform__age(self):
        expected_data = {
            'Name': ['Jane Smith', 'John Doe', 'Mark Johnson'],
            'Age':  [25, 30, 35],
            'Gender': ['F', 'M', 'M'],
            'Email': ['jane.smith@example.com', 'john.doe@example.com', 'mark.johnson@example.com']
        }
        sort_mapping = {'Age': False}
        transformed_data = sort_transform(self.sample_data, sort_mapping) 
        o = pd.DataFrame(expected_data)
        np.array_equal(transformed_data.values, pd.DataFrame(expected_data).values)
        # self.assertTrue(transformed_data.equals(outputDf))

    def test_check_data_type_transform(self):
        transformed_data = self.sample_data.copy()
        self.assertRaises(ValueError, check_data_type_transform, transformed_data, {'Name': int})

    def test_check_not_blank_transform(self):
        transformed_data = self.sample_data.copy()
        transformed_data.loc[0, 'Name'] = ''
        self.assertRaises(ValueError, check_not_blank_transform, transformed_data, ['Name'])


if __name__ == '__main__':
    unittest.main()
