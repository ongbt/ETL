from transform import apply_transformations
from parse_arguments import parse_arguments, parse_transformations_file
import pandas as pd


args = parse_arguments()
transformation_definitions = parse_transformations_file(args.transformations_file)

df = pd.read_csv(args.input_file)
df = apply_transformations(df, transformation_definitions)
df.to_csv(args.output_file, index=False)
