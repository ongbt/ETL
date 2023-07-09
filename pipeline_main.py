from pipeline import run_pipeline
from parse_transformations_file import parse_transformations_file
import argparse
import yaml 

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run pipeline based on pipeline definitions.')
    parser.add_argument('pipeline_definition_file', type=str, help='Pipeline file path') 
    args = parser.parse_args()
    return args

def parse_pipeline_definitions_file(pipeline_definition_file):
    with open(pipeline_definition_file, 'r') as file:
        pipeline_definitions = yaml.safe_load(file)
    return pipeline_definitions

args = parse_arguments() 
pipeline_definitions = parse_transformations_file(args.pipeline_definition_file)
run_pipeline(pipeline_definitions) 
