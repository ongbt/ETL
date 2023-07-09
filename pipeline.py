import pandas as pd
import yaml
from transform import apply_transformations
from parse_arguments import parse_arguments, parse_transformations_file


def merge(input_file1, input_file2, output_file, key_column):
    try:
        df1 = pd.read_csv(input_file1)
        df2 = pd.read_csv(input_file2)
        merged_df = pd.merge(df1, df2, on=key_column)
        merged_df.to_csv(output_file, index=False)
        print(f"Merged CSV files '{input_file1}' and '{input_file2}' into '{output_file}' successfully.")
    except (FileNotFoundError, KeyError) as e:
        print(f"Error occurred during merge: {str(e)}")

def split(input_file, output_definitions):
    try:
        df = pd.read_csv(input_file)
        for output_file, columns in output_definitions.items():
            split_df = df[columns]
            split_df.to_csv(output_file, index=False)
            print(f"Split CSV file '{input_file}' into '{output_file}' successfully.")
    except (FileNotFoundError, KeyError) as e:
        print(f"Error occurred during split: {str(e)}")

def process(input_file, transformation_file, output_file):
    try:
        df = pd.read_csv(input_file)
        transformation_definitions = parse_transformations_file(transformation_file)
        df = apply_transformations(df, transformation_definitions)
        df.to_csv(output_file, index=False)
    except (FileNotFoundError, KeyError) as e:
        print(f"Error occurred during split: {str(e)}")


def run_pipeline(pipeline_definitions):
    try:

        for pipeline_definition_item in pipeline_definitions:
            pipeline_definition_type = list(pipeline_definition_item.keys())[0]
            pipeline_definition = list(pipeline_definition_item.values())[0]    
            
            if pipeline_definition_type == 'merge':
                merge(
                    pipeline_definition['input_file1'],
                    pipeline_definition['input_file2'],
                    pipeline_definition['output_file'],
                    pipeline_definition['key_column']
                )
            elif pipeline_definition_type == 'split':
                split(
                    pipeline_definition['input_file'],
                    pipeline_definition['output_definitions'] 
                )
            elif pipeline_definition_type == 'process':
                process(
                    pipeline_definition['input_file'],
                    pipeline_definition['transformation_file'],
                    pipeline_definition['output_file']
                )
        # Perform additional processing on input_file if required 
    except (FileNotFoundError, KeyError, yaml.YAMLError) as e:
        print(f"Error occurred during CSV processing: {str(e)}")

 
 
# Example usage
# process('input.csv', 'transformations.yml', 'output.csv')
