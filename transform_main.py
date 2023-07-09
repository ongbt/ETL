from transform import apply_transformations
from parse_transformations_file import parse_transformations_file
import pandas as pd
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Transform input CSV file based on transformation definitions.')
    parser.add_argument('input_file', type=str, help='Input CSV file path')
    parser.add_argument('output_file', type=str, help='Output CSV file path')
    parser.add_argument('transformations_file', type=str, help='Transformation definitions file path')
    args = parser.parse_args()
    return args

args = parse_arguments()
transformation_definitions = parse_transformations_file(args.transformations_file)

df = pd.read_csv(args.input_file)
df = apply_transformations(df, transformation_definitions)
df.to_csv(args.output_file, index=False)
