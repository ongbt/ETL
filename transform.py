import pandas as pd


 
def split_transform(df, column, separator):
    if column not in df.columns:
        raise ValueError(f"Invalid column '{column}' specified for split_transform")
    split_values = df[column].str.split(separator, expand=True)
    for i, col in enumerate(split_values.columns):
        new_column_name = f'{column}_{i+1}'
        df.loc[:, new_column_name] = split_values[col]
    return df


def split_pair_transform(df, column, separator, first=True):
    if column not in df.columns:
        raise ValueError(f"Invalid column '{column}' specified for split_pair_transform")
    if first:
        split_values = df[column].str.split(separator, n=1, expand=True)
    else:
        split_values = df[column].str.rsplit(separator, n=1, expand=True)

    new_columns = [f'{column}_{i+1}' for i in range(split_values.shape[1])]
    df = pd.concat([df, split_values.rename(columns=dict(zip(split_values.columns, new_columns)))], axis=1)
    return df



def replace_transform(df, column, match_value, replacement):
    if column not in df.columns:
        raise ValueError(f"Invalid column '{column}' specified for replace_transform")
    df[column] = df[column].astype(str).str.replace(match_value, replacement)
    return df


def replace_text_transform(df, column, start_position, end_position, replacement_character, start=True):
    if column not in df.columns:
        raise ValueError(f"Invalid column '{column}' specified for replace_text_transform")
    df[column] = df[column].astype(str)
    length = df[column].str.len()

    def replace_text(row):
        text = row[column]
        length = len(text)

        if start:
            start_index = start_position
            end_index = min(end_position + 1, length)
        else:
            start_index = max(length - end_position - 1, 0)
            end_index = max(length - start_position, 0)

        num_replacements = end_index - start_index
        replacement_text = replacement_character * num_replacements

        replaced_text = text[:start_index] + replacement_text + text[end_index:]
        return replaced_text

    df[column] = df.apply(replace_text, axis=1)

    return df


def merge_transform(df, columns, output_column=None, separator=' '):
    merge_columns = [col.strip() for col in columns if col.strip() in df.columns]
    if not merge_columns:
        raise ValueError("No valid columns specified for merge_transform")
    if output_column is None:
        output_column = '_'.join(merge_columns)
    separator = separator
    merged_value = df[merge_columns].apply(lambda x: separator.join(x.dropna().astype(str)), axis=1)
    df[output_column] = merged_value
    return df


def filter_transform(df, columns):
    invalid_columns = [col for col in columns if col not in df.columns]
    if invalid_columns:
        raise ValueError(f"Invalid columns specified for filter_transform: {', '.join(invalid_columns)}")
    df = df[columns]
    return df


def filter_records_transform(df, condition):
    try:
        df = df.query(condition)
    except pd.core.computation.ops.UndefinedVariableError:
        raise ValueError(f"Invalid condition specified for filter_records_transform: {condition}")
    return df


def rename_transform(df, mapping):
    invalid_columns = [col for col in mapping if col not in df.columns]
    if invalid_columns:
        raise ValueError(f"Invalid columns specified for rename_transform: {', '.join(invalid_columns)}")
    df = df.rename(columns=mapping)
    return df


def map_value_transform(df, column, mapping, default_value=None):
    if column not in df.columns:
        raise ValueError(f"Invalid column '{column}' specified for map_value_transform")
    df.loc[:, column] = df[column].map(mapping)
    if default_value is not None:
        df.loc[:, column] = df[column].fillna(default_value)
    return df


def convert_case_transform(df, mapping):
    columns = [column for column in mapping if column in df.columns]
    if not columns:
        raise ValueError("No valid columns specified for convert_case_transform")
    for column in columns:
        if df[column].dtype == 'object':
            case_type = mapping[column]
            if case_type == 'uppercase':
                df.loc[:, column] = df[column].str.upper()
            elif case_type == 'lowercase':
                df.loc[:, column] = df[column].str.lower()
            elif case_type == 'titlecase':
                df.loc[:, column] = df[column].str.title()
            elif case_type == 'sentencecase':
                df.loc[:, column] = df[column].apply(lambda x: x.capitalize())
            else:
                raise ValueError(f"Invalid case '{case_type}' specified for column '{column}' in convert_case_transform")
    return df


def copy_columns_transform(df, mapping):
    invalid_columns = [col for col in mapping if col not in df.columns]
    if invalid_columns:
        raise ValueError(f"Invalid columns specified for copy_columns_transform: {', '.join(invalid_columns)}")
    for column in mapping:
        new_column_name = mapping[column]
        df[new_column_name] = df[column]
    return df


def sort_transform(df, mapping):
    columns = [col for col in mapping if col in df.columns]
    if not columns:
        raise ValueError("No valid columns specified for sort_transform")
    sort_orders = [mapping[col] for col in columns]

    invalid_orders = [order for order in sort_orders if not isinstance(order, bool)]
    if invalid_orders:
        raise ValueError(f"Invalid sort orders specified: {', '.join([str(order) for order in invalid_orders])}")

    df = df.sort_values(columns, ascending=sort_orders)
    return df


def check_data_type_transform(df, mapping):
    invalid_columns = [col for col in mapping if col not in df.columns]
    if invalid_columns:
        raise ValueError(f"Invalid columns specified for check_data_type_transform: {', '.join(invalid_columns)}")

    for column in mapping:
        expected_data_type = mapping[column]
        if df[column].dtype != expected_data_type:
            raise ValueError(
                f"Invalid data type in column '{column}'. Expected data type: {expected_data_type}, found: {df[column].dtype}"
            )

    return df


def check_not_blank_transform(df, columns):
    invalid_columns = [col for col in columns if col not in df.columns]
    if invalid_columns:
        raise ValueError(f"Invalid columns specified for check_not_blank_transform: {', '.join(invalid_columns)}")

    for column in columns:
        if df[column].isnull().any() or (df[column] == '').any():
            raise ValueError(f"Blank values found in column '{column}'")

    return df


def apply_transformations(df, transformation_definitions):
    for transformation_definition in transformation_definitions:
        transformation_type = list(transformation_definition.keys())[0]
        transformation = list(transformation_definition.values())[0]

        if transformation_type == 'split':
            df = split_transform(df, transformation['column'], transformation['separator'])
        elif transformation_type == 'split_pair':
            df = split_pair_transform(df, transformation['column'], transformation['separator'], transformation['first'])
        elif transformation_type == 'replace':
            df = replace_transform(df, transformation['column'], transformation['match_value'], transformation['replacement'])
        elif transformation_type == 'replace_text':
            df = replace_text_transform(df, transformation['column'], transformation['start_position'], transformation['end_position'], transformation['replacement'], transformation['start'])
        elif transformation_type == 'merge':
            df = merge_transform(df, transformation['columns'], transformation.get('output_column'), transformation.get('separator'))
        elif transformation_type == 'filter':
            df = filter_transform(df, transformation['columns'])
        elif transformation_type == 'filter_records':
            df = filter_records_transform(df, transformation['condition'])
        elif transformation_type == 'rename':
            df = rename_transform(df, transformation['mapping'])
        elif transformation_type == 'map_value':
            df = map_value_transform(df, transformation['column'], transformation['mapping'], transformation['default_value'])
        elif transformation_type == 'convert_case':
            df = convert_case_transform(df, transformation['mapping'])
        elif transformation_type == 'copy_columns':
            df = copy_columns_transform(df, transformation['mapping'])
        elif transformation_type == 'sort':
            df = sort_transform(df, transformation['mapping'])
        elif transformation_type == 'check_data_type':
            df = check_data_type_transform(df, transformation['mapping'])
        elif transformation_type == 'check_not_blank':
            df = check_not_blank_transform(df, transformation['columns'])

    return df
