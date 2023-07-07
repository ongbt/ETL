import argparse
import pandas as pd
import yaml
import re


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


def transform_replace_value(df, column_definition):
    column = column_definition['column']
    pattern = column_definition['pattern']
    replacement = column_definition['replacement']
    df.loc[:, column] = df[column].apply(lambda x: re.sub(pattern, replacement, str(x)))

def transform_split_advanced(df, column_definition):
    split_column = column_definition['column']
    delimiter = column_definition['delimiter']
    split_type = column_definition.get('split_type', 'first')

    if split_type == 'first':
        split_values = df[split_column].str.split(delimiter, n=1, expand=True)
    elif split_type == 'last':
        split_values = df[split_column].str.rsplit(delimiter, n=1, expand=True)
    else:
        print(f"Error: Invalid split_type '{split_type}' specified for column '{split_column}'. Using 'first' split type.")
        split_values = df[split_column].str.split(delimiter, n=1, expand=True)

    for i, col in enumerate(split_values.columns):
        df[f'{split_column}_{i+1}'] = split_values[col]

 
def transform_replace_first_last(df, column_definition):
    column = column_definition['column']
    num_chars = column_definition['num_chars']
    replacement = column_definition['replacement']
    mode = column_definition.get('mode', 'first')

    if mode == 'first':
        df[column] = df[column].apply(lambda x: replacement + x[num_chars:])
    elif mode == 'last':
        df[column] = df[column].apply(lambda x: x[:-num_chars] + replacement)
    else:
        print(f"Error: Invalid mode '{mode}' specified for column '{column}'. Using 'first' mode.")


def transform_convert_case(df, column_definition):
    convert_column = column_definition['column']
    case = column_definition['case']

    if case == 'uppercase':
        df[convert_column] = df[convert_column].str.upper()
    elif case == 'lowercase':
        df[convert_column] = df[convert_column].str.lower()
    elif case == 'titlecase':
        df[convert_column] = df[convert_column].str.title()
    elif case == 'sentencecase':
        df[convert_column] = df[convert_column].apply(lambda x: x.capitalize())
    else:
        print(f"Error: Invalid case '{case}' specified for column '{convert_column}'. Using original case.")


def transform_convert_case(df, column_definition):
    columns = column_definition['columns']
    case_type = column_definition['case_type']

    for column in columns:
        if case_type == 'uppercase':
            df[column] = df[column].str.upper()
        elif case_type == 'lowercase':
            df[column] = df[column].str.lower()
        elif case_type == 'titlecase':
            df[column] = df[column].str.title()
        elif case_type == 'sentencecase':
            df[column] = df[column].apply(lambda x: x[0].upper() + x[1:].lower() if isinstance(x, str) else x)
        else:
            print(f"Error: Invalid case type '{case_type}' specified for column '{column}'.")


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
        elif transformation_type == 'replace_value':
            transform_replace_value(df, column_definition)           
        elif transformation_type == 'split_advanced':
            transform_split_advanced(df, column_definition)  
        elif transformation_type == 'replace_first_last':
            transform_replace_first_last(df, column_definition)
        elif transformation_type == 'convert_case':
            transform_convert_case(df, column_definition)
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
