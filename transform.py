import pandas as pd


def split_transform(df, column, separator):
    split_values = df[column].str.split(separator, expand=True)
    for i, col in enumerate(split_values.columns):
        df[f'{column}_{i+1}'] = split_values[col]
    return df


def split_pair_transform(df, column, separator, first=True):
    if first:
        split_values = df[column].str.split(separator, n=1, expand=True)
    else:
        split_values = df[column].str.rsplit(separator, n=1, expand=True)

    for i, col in enumerate(split_values.columns):
        df[f'{column}_{i+1}'] = split_values[col]
    return df


def replace_transform(df, column, match_value, replacement):
    df[column] = df[column].astype(str).str.replace(match_value, replacement)
    return df


def replace_characters_transform0(df, column, num_characters, replacement, first=True):
    df[column] = df[column].astype(str)
    if first:
        # df[column] = df[column].str[:num_characters] + replacement + df[column].str[num_characters:]
        df[column] = df[column].apply(lambda x: replacement + x[num_characters:])
    else:
        # df[column] = df[column].str[:-num_characters] + replacement + df[column].str[-num_characters:]
        df[column] = df[column].apply(lambda x: x[:-num_characters] + replacement)
    return df
def replace_text_transform(df, column, start_position, end_position, replacement_character, start=True):
    df[column] = df[column].astype(str)

    def replace_text(row):
        text = row[column]
        length = len(text)

        if start:
            start_index = start_position
            end_index = min(end_position + 1, length)
        else:
            start_index = max(length - end_position - 1, 0)
            end_index = max(length - start_position, 0)

        # Check if start_position and end_position are within range
        if start_index > length or end_index > length or start_index > end_index:
            raise ValueError(f"Invalid start_position or end_position specified for column '{column}'")

        num_replacements = end_index - start_index
        replacement_text = replacement_character * num_replacements

        replaced_text = text[:start_index] + replacement_text + text[end_index:]
        return replaced_text

    df[column] = df.apply(replace_text, axis=1)

    return df


def merge_transform0(df, column1, column2, output_column=None, separator=' '):
    if output_column is None:
        output_column = column1 + '_' + column2
    df[output_column] = df[column1] + separator + df[column2]
    return df

def merge_transform(df, columns, output_column=None, separator=' '):
    merge_columns = [col.strip() for col in columns if col.strip() in df.columns]
    if output_column is None:
        output_column =  '_'.join(merge_columns)
    separator = separator
    merged_value = df[merge_columns].apply(lambda x: separator.join(x.dropna().astype(str)), axis=1)
    df[output_column] = merged_value
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


def map_value_transform(df, column, mapping, default_value=None):
    df[column] = df[column].map(mapping)
    if default_value is not None:
        df[column].fillna(default_value, inplace=True)
    return df



def convert_case_transform(df, mapping):

    columns = [column for column in mapping]
    for column in columns:
        if df[column].dtype == 'object':
            case_type = mapping[column]
            if case_type == 'uppercase':
                df[column] = df[column].str.upper()
            elif case_type == 'lowercase':
                df[column] = df[column].str.lower()
            elif case_type == 'titlecase':
                df[column] = df[column].str.title()
            elif case_type == 'sentencecase':
                df[column] = df[column].apply(lambda x: x.capitalize())
            else:
                print(f"Error: Invalid case '{case_type}' specified for column '{column}'. Using original case.")
    return df

def copy_columns_transform(df, mapping):
    for column in mapping:
        new_column_name = mapping[column]
        df[new_column_name] = df[column]
    return df


def sort_transform(df, mapping):
    columns = [col for col in mapping]
    sort_orders = [mapping[col] for col in columns]

    # Validate columns in the mapping exist in the DataFrame
    invalid_columns = [col for col in columns if col not in df.columns]
    if invalid_columns:
        raise ValueError(f"Invalid columns specified for sorting: {', '.join(invalid_columns)}")

    # Validate sort orders in the mapping
    invalid_orders = [order for order in sort_orders if not isinstance(order, bool)]
    if invalid_orders:
        raise ValueError(f"Invalid sort orders specified: {', '.join([str(order) for order in invalid_orders])}")

    # Perform the sorting
    df = df.sort_values(columns, ascending=sort_orders)

    return df


def apply_transformations(df, transformation_definitions):
    for transformation_definition in transformation_definitions:
        # transformation_type = transformation['type']

        transformation_type = list(transformation_definition.keys())[0]
        transformation = list(transformation_definition.values())[0]
        
        if transformation_type == 'split':
            df = split_transform(df, transformation['column'], transformation['separator'])
        elif transformation_type == 'split_pair':
            df = split_pair_transform(df, transformation['column'], transformation['separator'], transformation['first'])
        elif transformation_type == 'replace':
            df = replace_transform(df, transformation['column'], transformation['match_value'], transformation['replacement'])
        # elif transformation_type == 'replace_characters':
        #     df = replace_characters_transform(df, transformation['column'], transformation['num_characters'], transformation['replacement'], transformation['first'])
        elif transformation_type == 'replace_text':
            df = replace_text_transform(df, transformation['column'], transformation['start_position'], transformation['end_position'], transformation['replacement'], transformation['start'])
        elif transformation_type == 'merge':
            df = merge_transform(df, transformation['columns'], transformation.get('output_column'), transformation.get('separator'))
        elif transformation_type == 'filter_columns':
            df = filter_columns_transform(df, transformation['columns'])
        elif transformation_type == 'filter_records':
            df = filter_records_transform(df, transformation['condition'])
        elif transformation_type == 'rename_column':
            df = rename_columns_transform(df, transformation['mapping'])
        elif transformation_type == 'map_value':
            df = map_value_transform(df, transformation['column'], transformation['mapping'], transformation['default_value'])
        elif transformation_type == 'convert_case':
            # df = convert_case_transform(df, transformation['columns'], transformation['case_type'])
            df = convert_case_transform(df, transformation['mapping'])
        elif transformation_type == 'copy_columns':
            # df = copy_column_transform(df, transformation['column'], transformation['new_column'])
            df = copy_columns_transform(df, transformation['mapping'])
        elif transformation_type == 'sort':
            # df = sort_transform(df, transformation['columns'], transformation['sort_ascending'])
            df = sort_transform(df, transformation['mapping'])
    return df
