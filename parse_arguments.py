import argparse
import yaml


def parse_arguments():
    parser = argparse.ArgumentParser(description='Transform input CSV file based on transformation definitions.')
    parser.add_argument('input_file', type=str, help='Input CSV file path')
    parser.add_argument('output_file', type=str, help='Output CSV file path')
    parser.add_argument('transformations_file', type=str, help='Transformation definitions file path')
    args = parser.parse_args()
    return args


def parse_transformations_file(transformations_file):
    with open(transformations_file, 'r') as file:
        transformations = yaml.safe_load(file)
    return transformations
