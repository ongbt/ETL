import unittest
import pandas as pd
from program import transform_csv

class CsvTransformationTestCase(unittest.TestCase):
    def test_merge_transformation(self):
        input_data = pd.DataFrame({'Name': ['John Doe', 'Jane Smith'],
                                   'Age': [25, 30],
                                   'Email': ['johndoe@example.com', 'janesmith@example.com'],
                                   'Phone': ['1234567890', '9876543210']})
        expected_output = pd.DataFrame({'Name': ['John Doe', 'Jane Smith'],
                                        'Age': [25, 30],
                                        'Email': ['johndoe@example.com', 'janesmith@example.com'],
                                        'Phone': ['1234567890', '9876543210'],
                                        'NameAndAge': ['John Doe_25', 'Jane Smith_30']})
        transform_csv('input.csv', 'output.csv', 'transformations.yml')
        output_data = pd.read_csv('output.csv')
        pd.testing.assert_frame_equal(output_data, expected_output)

    def test_filter_columns_transformation(self):
        input_data = pd.DataFrame({'Name': ['John Doe', 'Jane Smith'],
                                   'Age': [25, 30],
                                   'Email': ['johndoe@example.com', 'janesmith@example.com'],
                                   'Phone': ['1234567890', '9876543210']})
        expected_output = pd.DataFrame({'Name': ['John Doe', 'Jane Smith'],
                                        'Email': ['johndoe@example.com', 'janesmith@example.com']})
        transform_csv('input.csv', 'output.csv', 'transformations.yml')
        output_data = pd.read_csv('output.csv')
        pd.testing.assert_frame_equal(output_data, expected_output)

    def test_filter_records_transformation(self):
        input_data = pd.DataFrame({'Name': ['John Doe', 'Jane Smith'],
                                   'Age': [25, 30],
                                   'Email': ['johndoe@example.com', 'janesmith@example.com'],
                                   'Phone': ['1234567890', '9876543210']})
        expected_output = pd.DataFrame({'Name': ['John Doe'],
                                        'Age': [25],
                                        'Email': ['johndoe@example.com'],
                                        'Phone': ['1234567890']})
        transform_csv('input.csv', 'output.csv', 'transformations.yml')
        output_data = pd.read_csv
