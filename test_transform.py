import pandas as pd
import unittest

from transform import *

import pandas as pd
import unittest

class DataFrameTransformationTests(unittest.TestCase):

    def setUp(self):
        data = {'Name': ['John Doe', 'Jane Smith'],
                'Age': [30, 25],
                'Location': ['New York', 'Los Angeles']}
        self.df = pd.DataFrame(data)

    def test_split_transform(self):
        transformed_df = split_transform(self.df, 'Name', ' ')
        self.assertEqual(transformed_df['Name_1'][0], 'John')
        self.assertEqual(transformed_df['Name_2'][0], 'Doe')
        self.assertEqual(transformed_df['Name_1'][1], 'Jane')
        self.assertEqual(transformed_df['Name_2'][1], 'Smith')

    def test_split_pair_transform(self):
        transformed_df = split_pair_transform(self.df, 'Name', ' ', first=True)
        self.assertEqual(transformed_df['Name_1'][0], 'John')
        self.assertEqual(transformed_df['Name_2'][0], 'Doe')
        transformed_df = split_pair_transform(self.df, 'Name', ' ', first=False)
        self.assertEqual(transformed_df['Name_1'][1], 'Jane')
        self.assertEqual(transformed_df['Name_2'][1], 'Smith')

    def test_replace_transform(self):
        transformed_df = replace_transform(self.df, 'Location', 'New', 'Old')
        self.assertEqual(transformed_df['Location'][0], 'Old York')
        self.assertEqual(transformed_df['Location'][1], 'Los Angeles')

    def test_replace_characters_transform(self):
        transformed_df = replace_characters_transform(self.df, 'Name', 4, 'X', first=True)
        self.assertEqual(transformed_df['Name'][0], 'JohnXoe')
        transformed_df = replace_characters_transform(self.df, 'Name', 4, 'X', first=False)
        self.assertEqual(transformed_df['Name'][1], 'JaneXmith')

    def test_merge_transform(self):
        transformed_df = merge_transform(self.df, ['Name', 'Location'], output_column='Full_Name', separator='_')
        self.assertEqual(transformed_df['Full_Name'][0], 'John Doe_New York')
        self.assertEqual(transformed_df['Full_Name'][1], 'Jane Smith_Los Angeles')

    def test_filter_columns_transform(self):
        transformed_df = filter_columns_transform(self.df, ['Name', 'Age'])
        self.assertTrue('Name' in transformed_df.columns)
        self.assertTrue('Age' in transformed_df.columns)
        self.assertFalse('Location' in transformed_df.columns)

    def test_filter_records_transform(self):
        transformed_df = filter_records_transform(self.df, "Age > 25")
        self.assertEqual(len(transformed_df), 1)
        self.assertEqual(transformed_df['Name'][0], 'John Doe')

    def test_rename_columns_transform(self):
        transformed_df = rename_columns_transform(self.df, {'Name': 'Full_Name', 'Age': 'Years'})
        self.assertTrue('Full_Name' in transformed_df.columns)
        self.assertTrue('Years' in transformed_df.columns)
        self.assertFalse('Name' in transformed_df.columns)
        self.assertFalse('Age' in transformed_df.columns)

    def test_map_value_transform(self):
        mapping = {'New York': 'NY', 'Los Angeles': 'LA'}
        transformed_df = map_value_transform(self.df, 'Location', mapping, default_value='Unknown')
        self.assertEqual(transformed_df['Location'][0], 'NY')
        self.assertEqual(transformed_df['Location'][1], 'LA')
        transformed_df = map_value_transform(self.df, 'Location', {'Chicago': 'IL'}, default_value='Unknown')
        self.assertEqual(transformed_df['Location'][0], 'Unknown')
        self.assertEqual(transformed_df['Location'][1], 'Unknown')

    def test_convert_case_transform(self):
        mapping = {'Name': 'titlecase'}
        transformed_df = convert_case_transform(self.df, mapping)
        self.assertEqual(transformed_df['Name'][0], 'John Doe')
        self.assertEqual(transformed_df['Name'][1], 'Jane Smith')

    def test_copy_columns_transform(self):
        transformed_df = copy_columns_transform(self.df, {'Name': 'Full_Name', 'Age': 'Years'})
        self.assertTrue('Full_Name' in transformed_df.columns)
        self.assertTrue('Years' in transformed_df.columns)
        self.assertEqual(transformed_df['Full_Name'][0], 'John Doe')
        self.assertEqual(transformed_df['Full_Name'][1], 'Jane Smith')
        self.assertEqual(transformed_df['Years'][0], 30)
        self.assertEqual(transformed_df['Years'][1], 25)

    def test_sort_transform(self):
        # mapping = {'Name': True, 'Age': False}
        mapping = {'Age': True}
        transformed_df = sort_transform(self.df, mapping)
        self.assertEqual(transformed_df['Name'][0], 'Jane Smith')
        self.assertEqual(transformed_df['Name'][1], 'John Doe')

    def test_apply_transformations(self):
        transformations = [
            {'split': {'column': 'Name', 'separator': ' '}},
            {'replace': {'column': 'Location', 'match_value': 'New', 'replacement': 'Old'}},
            {'merge': {'columns': ['Name_1', 'Name_2'], 'output_column': 'Full_Name', 'separator': '_'}},
            {'filter_columns': {'columns': ['Full_Name', 'Age']}},
            {'filter_records': {'condition': 'Age > 25'}},
            {'rename_column': {'mapping': {'Full_Name': 'Name', 'Age': 'Years'}}},
            {'map_value': {'column': 'Name', 'mapping': {'John_Doe': 'JD'}, 'default_value': 'Unknown'}},
            {'convert_case': {'mapping': {'Name': 'uppercase'}}},
            {'copy_columns': {'mapping': {'Name': 'Full_Name', 'Years': 'Age'}}},
            {'sort': {'mapping': {'Full_Name': True, 'Age': False}}}
        ]

        transformed_df = apply_transformations(self.df, transformations)

        self.assertTrue('Full_Name' in transformed_df.columns)
        self.assertTrue('Age' in transformed_df.columns)
        self.assertTrue('Name' in transformed_df.columns)
        self.assertFalse('Location' in transformed_df.columns)
        self.assertEqual(len(transformed_df), 1)
        self.assertEqual(transformed_df['Age'][0], 30)
        self.assertFalse('Name_1' in transformed_df.columns)
        self.assertFalse('Name_2' in transformed_df.columns)
        self.assertEqual(transformed_df['Full_Name'][0], 'JD')

if __name__ == '__main__':
    unittest.main()
