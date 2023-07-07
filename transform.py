import pandas as pd


def split_transform(df, column, separator):
    split_values = df[column].str.split(separator, expand=True)
    for i, col in enumerate(split_values.columns):
        df[f'{column}_{i+1}'] = split_values[col]
    return df


def split_pair_transform(df, column, separator, first=True):
    if first:
        df[column] = df[column].str.split(separator).str[0]
    else:
        df[column] = df[column].str.rsplit(separator, n=1).str[-1]
    return df


def replace_transform(df, column, match_value, replacement):
    df[column] = df[column].astype(str).str.replace(match_value, replacement)
    return df


def replace_characters_transform(df, column, num_characters, replacement, first=True):
    df[column] = df[column].astype(str)
    if first:
        df[column] = df[column].str[:num_characters] + replacement + df[column].str[num_characters:]
    else:
        df[column] = df[column].str[:-num_characters] + replacement + df[column].str[-num_characters:]
    return df


def merge_transform(df, column1, column2, output_column=None, separator=' '):
    if output_column is None:
        output_column = column1 + '_' + column2
    df[output_column] = df[column1] + separator + df[column2]
    return df


def filter_columns_transform(df, columns):
    df = df[columns]
    return df


def filter_records_transform(df, condition):
    df = df.query(condition)
    return df


def rename_columns_transform(df, mapping):
    df = df.rename(columns=mapping)
    return df


def map_value_transform(df, column, mapping):
    df[column] = df[column].map(mapping)
    return df


def convert_case_transform(df, columns, case_type):
    for column in columns:
        if df[column].dtype == 'object':
            if case_type == 'uppercase':
                df[column] = df[column].str.upper()
            elif case_type == 'lowercase':
                df[column] = df[column].str.lower()
            elif case_type == 'titlecase':
                df[column] = df[column].str.title()
            elif case_type == 'sentencecase':
                df[column] = df[column].apply(lambda x: x[0].upper() + x[1:].lower())
    return df


def apply_transformations(df, transformations):
    for transformation in transformations:
        transformation_type = transformation['type']
        if transformation_type == 'split':
            df = split_transform(df, transformation['column'], transformation['separator'])
        elif transformation_type == 'split_pair':
            df = split_pair_transform(df, transformation['column'], transformation['separator'], transformation['first'])
        elif transformation_type == 'replace':
            df = replace_transform(df, transformation['column'], transformation['match_value'], transformation['replacement'])
        elif transformation_type == 'replace_characters':
            df = replace_characters_transform(df, transformation['column'], transformation['num_characters'], transformation['replacement'], transformation['first'])
        elif transformation_type == 'merge':
            df = merge_transform(df, transformation['column1'], transformation['column2'], transformation.get('output_column'), transformation.get('separator'))
        elif transformation_type == 'filter_columns':
            df = filter_columns_transform(df, transformation['columns'])
        elif transformation_type == 'filter_records':
            df = filter_records_transform(df, transformation['condition'])
        elif transformation_type == 'rename_column':
            df = rename_columns_transform(df, transformation['mapping'])
        elif transformation_type == 'map_value':
            df = map_value_transform(df, transformation['column'], transformation['mapping'])
        elif transformation_type == 'convert_case':
            df = convert_case_transform(df, transformation['columns'], transformation['case_type'])
    return df
