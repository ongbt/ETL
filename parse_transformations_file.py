
import yaml




def parse_transformations_file(transformations_file):
    with open(transformations_file, 'r') as file:
        transformations = yaml.safe_load(file)
    return transformations
