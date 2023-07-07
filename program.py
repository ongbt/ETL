import argparse
import pandas as pd
import yaml


def transform_merge(df, column_definition):
    merge_columns = [col.strip() for col in column_definition['columns'] if col.strip() in df.columns]
    output_column_name = column_definition.get('output_column', '_'.join(merge_columns))
    separator = column_definition.get('separator', '')
    merged_value = df[merge_columns].apply(lambda x: separator.join(x.dropna().astype(str)), axis=1)
    df[output_column_name] = merged_value


def transform_split(df, column_definition):
    split_column = column_definition['column']
    delimiter = column_definition['delimiter']
    split_values = df[split_column].str.split(delimiter, expand=True)
    for i, col in enumerate(split_values.columns):
        df[f'{split_column}_{i+1}'] = split_values[col]


def transform_convert(df, column_definition):
    convert_column = column_definition
    df[convert_column] = df[convert_column].astype(int)


def transform_rename(df, column_definition):
    column_mapping = column_definition.get('mapping', {})
    for old_name, new_name in column_mapping.items():
        df.rename(columns={old_name: new_name}, inplace=True)


def transform_filter_columns(df, column_definition):
    columns_to_keep = column_definition['columns']
    df = df[columns_to_keep]
    return df


def transform_filter_records(df, column_definition):
    column = column_definition['column']
    operator = column_definition['operator']
    value = column_definition['value']
    df = df.query(f"{column} {operator} {value}")
    return df


def transform_map_values(df, column_definition):
    column = column_definition['column']
    mapping = column_definition['mapping']
    df[column] = df[column].apply(lambda x: mapping.get(x, x))

def apply_transformations(df, transformations):
    for transformation in transformations:
        transformation_type = list(transformation.keys())[0]
        column_definition = list(transformation.values())[0]

        if transformation_type == 'merge':
            transform_merge(df, column_definition)
        elif transformation_type == 'split':
            transform_split(df, column_definition)
        elif transformation_type == 'convert':
            transform_convert(df, column_definition)
        elif transformation_type == 'rename':
            transform_rename(df, column_definition)
        elif transformation_type == 'filter_columns':
            df = transform_filter_columns(df, column_definition)
        elif transformation_type == 'filter_records':
            df = transform_filter_records(df, column_definition)
        elif transformation_type == 'map_values':
            transform_map_values(df, column_definition)
        # Add more transformation types as needed

    return df


def transform_csv(input_file, output_file, transformation_file, encoding='utf-8'):
    # Read the input CSV file into a pandas DataFrame, handling encoding errors
    try:
        df = pd.read_csv(input_file, encoding=encoding)
    except UnicodeDecodeError:
        print(f"Error: Failed to decode the input file '{input_file}' using encoding '{encoding}'.")
        return

    # Read the transformation definitions from the YAML file
    with open(transformation_file, 'r', encoding=encoding) as file:
        transformations = yaml.safe_load(file)

    # Perform transformations
    df = apply_transformations(df, transformations)

    # Write the transformed DataFrame to the output CSV file
    df.to_csv(output_file, index=False)

    print("Transformation complete. Output CSV file created.")


# Parse command line arguments
parser = argparse.ArgumentParser(description='CSV Transformation')
parser.add_argument('input_file', help='Path to the input CSV file')
parser.add_argument('output_file', help='Path to the output CSV file')
parser.add_argument('transformation_file', help='Path to the transformation definition YAML file')
parser.add_argument('--encoding', help='Encoding of the input and transformation files', default='utf-8')
args = parser.parse_args()

# Perform the CSV transformation
transform_csv(args.input_file, args.output_file, args.transformation_file, args.encoding)
