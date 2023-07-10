 

This user guide provides an overview of the data transformation program and explains how to use each transformation function. The program is designed to perform various data transformations on a Pandas DataFrame.

# Table of Contents 

- [Introduction](#introduction)
- [Pipeline](#pipeline)
  - [Example](#example)
- [Pipeline Definitions](#pipeline-definitions)
- [merge file](#merge-file)
- [split file](#split-file)
- [process file](#process-file)
- [Processing](#processing)
  - [check_data_type](#check_data_type)
  - [check_not_blank](#check_not_blank)
  - [checks](#checks)
- [Transformations](#transformations)
  - [duplicate](#duplicate)
  - [split](#split)
  - [split_pair](#split_pair)
  - [replace](#replace)
  - [replace_text](#replace_text)
  - [merge](#merge)
  - [drop](#drop)
  - [filter_records](#filter_records)
  - [map_value](#map_value)
  - [convert_case](#convert_case)
  - [rename](#rename)
  - [sort](#sort)

You can use these links to navigate directly to each section in your user guide.
# Introduction
ChatGPT: https://chat.openai.com/?model=text-davinci-002-render-sha

The data transformation program provides a collection of functions to manipulate and transform data in a Pandas DataFrame. These functions allow you to split, replace, merge, filter, rename, map values, convert case, copy columns, sort, and perform data type and blank value checks.


---

# Pipeline
## Example
```
- merge:
    input_file1: input1.csv
    input_file2: input2.csv
    output_file: merged.csv
    key_column: SSN

- process:
    input_file: merged.csv
    transformation_file: transformations.yml
    transformations: 
      ...
    output_file: processed.csv

- split:
    input_file: processed.csv
    output_definitions:
      split1.csv: [SSN, Name, Age, Email, ZipCode, Address]
      split2.csv: [SSN, Name, Phone, Sex]

```
## Pipeline Definitions
The Pipeline allows you to perform various transformations on files. It uses the pandas library for data manipulation and a YAML file to define the transformations. This guide will walk you through the usage of the provided functions and demonstrate an example usage.


### merge file
Merges two files based on a common key column.

#### Syntax:
```
- merge:
    input_file1: <input_file1>
    input_file2: <input_file2>
    output_file: <output_file>
    key_column: <key_column>
```
#### Parameters::
- input_file1: Path to the first input file.
- input_file2: Path to the second input file.
- output_file: Path to the output merged file.
- key_column: The common key column used for merging.
#### Example:
```
- merge:
    input_file1: input1.csv
    input_file2: input2.csv
    output_file: merged.csv
    key_column: SSN
 
```
---
### split file
Splits a file into multiple output files based on specified columns.

#### Syntax:
```
- split:
    input_file: <input_file>
    output_definitions:
      <output_file>: [<column>, <column>, ...]
      <output_file>: [<column>, <column>, ...]
      ...
```
#### Parameters::
- input_file: Path to the input file.
- output_definitions: A dictionary where keys are output file paths, and values are lists of columns to include in each output file.
  - output_file: Path to the output merged file. 
  - column: list - The list of column names to include in the output file.

#### Example:
```
- split:
    input_file: processed.csv
    output_definitions:
      split1.csv: [SSN, Name, Age, Email, ZipCode, Address]
      split2.csv: [SSN, Name, Phone, Sex]
```
---
### process file
Processes a file using transformations defined in a YAML file.

#### Syntax:
``` 
- process:
    input_file: <input_file>
    transformation_file: <transformation_file>
    transformations: 
      ...
    output_file:  <output_file> 
```
#### Parameters:
- input_file: Path to the input file.
- transformation_file: Path to the YAML file containing transformation definitions.
- output_file: Path to the output processed file.
- transformations: see [Processing](#processing)

#### Example:
```
- process:
    input_file: merged.csv
    transformation_file: transformations.yml
    output_file: processed.csv
 
```
---
# Processing
## Checks
### check_data_type
This function checks the data types of specified columns in the DataFrame.


#### Syntax:
```
- check_data_type:
    mapping:
      <column>: <data_type>
      ...
```

#### Parameters:
- mapping: dict - The dictionary specifying the column names as keys and the expected data types as values. The data types can be any valid Pandas data types.
  - data_type options: object | int64 | datetime64
#### Example:
```
- check_data_type:
    mapping:
      Name: object
      Age: int64
      Email: object
      City: object
      Address: object
      Sex: object
```
---
### check_not_blank
This function checks if specified columns have any blank values (NaN or empty strings).


#### Syntax:
```
- check_not_blank:
    columns: [<column>, <column>, ...]
```
#### Parameters:
- columns: list - The list of column names to check for blank values.

#### Example:
```
- check_not_blank:
    columns: [Name, Age, Phone, City, Address, ZipCode, Sex]
```

---
### checks
 


#### Syntax:
```
- checks:
    - type: length
      column: <column>
      max_length: <max_length>
    - type: values
      column: <column>
      valid_values: [<value>, >value>, ...]
    - type: not_blank
      columns: [<column>, <column>, ...]
    - type: range
      column: <column>
      min_value: <min_value>
      max_value: <max_value>
```
#### Parameters:
- type: length | values | not_blank | range

#### Example:
```
- checks:
    - type: length
      column: Name
      max_length: 100
    - type: values
      column: Sex
      valid_values:
        - M
        - F
    - type: not_blank
      columns:
        - Name
    - type: range
      column: Age
      min_value: 18
      max_value: 39
```

---
### create
 

#### Syntax:
```
- create:
    column: <new_column_name>
    data_type: <data_type>
    default_value: <default_value>

```
#### Parameters:
- column: The name of the new column to create.
- data_type: The desired data type for the new column.
- default_value (optional): The default value to assign to the new column. If not provided, the column will be left as blank.

#### Example:
```
- create:
    column: Income
    data_type: int64
    default_value: 3000

```
---

## Transformations
### duplicate
This function copies the values from specified columns to new columns with different names.


#### Syntax:
```
- duplicate:
    mapping:
      <column>: <new_column_name>
      ...
```
#### Parameters:
- mapping: dict - The dictionary specifying the original column names as keys and the new column names as values.
  - column: column to copy
  - new_column_name: name for the new column 
#### Example:
```
- duplicate:
    mapping:
      Name: Name_new
      Age: Age_new
      Email: Email_new
      Phone: Phone_new
      City: City_new
      Address: Address_new
      ZipCode: ZipCode_new
      Sex: Sex_new
```
---
### split
This function splits the values in a specified column into mulitple parts based on a separator and creates new columns with the split values. Each new column created will be named '{column}_{index}'.



#### Syntax:
```
- split:
    column: <column>
    separator: <separator_text>
```
#### Parameters:
- column: str - The column name to split. Muliple columns may be created.
- separator: str - The separator to split the values.
#### Example:
```
- split:
    column: City
    separator: " "
```
---
### split_pair
This function splits the values in a specified column into two parts based on a separator and creates new columns with the split values.

 
#### Syntax:
```
- split_pair:
    column: <column>
    separator: <separator_text>
    first:  True | False
```
#### Parameters:
- column: str - The column name to split. At most 2 columns will be created.
- separator: str - The separator to split the values.
- first: bool (optional) - Indicates whether to split from the first occurrence of the separator. Default is True.

#### Example:
```
- split_pair:
    column: Name
    separator: " "
    first: false
```
---
### replace
This function replaces values in a specified column with a new value.


#### Syntax:
```
- replace:
    column: <column>
    match: <match>
    replacement: <replacement_value>
``` 
#### Parameters:
- column: str - The column name to replace values.
- match: str - The value to match.
- replacement: str - The new value to replace with.
#### Example:
```
- replace:
    column: Phone_new
    match: "555"
    replacement: "XXX"

```
---
### replace_text
This function replaces a portion of text in a specified column with a replacement character.
#### Syntax:
```
- replace_text:
    column: <column>
    start_position: <start_position>
    end_position: <end_position>
    replacement: <replacement_text>
    start: True | False
```
#### Parameters:
- column: str - The column name to replace text.
- start_position: int - The starting position of the text to replace.
- end_position: int - The ending position of the text to replace.
- replacement: str - The character to use for replacement.
- start: bool (optional) - Indicates whether the start position is counted from the beginning or end of the text. Default is True.

#### Example:
```
- replace_text:
    column: Phone_new
    start_position: 1
    end_position: 2
    replacement: "^"
    start: false

```
---
### merge
This function merges the values of multiple columns into a single column.


#### Syntax:
``` 
- merge:
    columns: [<column>, <column>, ...]
    separator: <separator_text>
    output_column: <new_column_name>
```
#### Parameters:
- columns: list - The list of column names to merge. You can merge multiple columns.
- output_column: str (optional) - The name of the output column. If not provided, the merged column name will be generated.
- separator: str (optional) - The separator to use between merged values. Default is a space (' ').
#### Example:
```
- merge:
    columns: [Address, City, ZipCode]
    separator: ", "
    output_column: "Address City ZipCode"
```
---
### drop
This function drop columns from the table.

#### Syntax:
```
- drop:
    columns: [<column>, <column>, ...]
```
#### Parameters:
- columns: list - The list of column names to be dropped.

#### Example:
```
- drop:
    columns: [Age, Name]
```

---
### filter_records
This function filters the DataFrame based on a condition.
See https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html for condition

#### Syntax:
```
- filter_records:
    condition: <condition>
```
#### Parameters:
- condition: The filtering condition written as a string.

#### Example:
```
- filter_records:
    condition: "(Age <= 30) and (ZipCode >= 50000)"
```
---
### map_value
This function maps the values in a specified column to new values based on a mapping dictionary.


``` 
- map_value:
    column: <column>
    default_value: <default_value>
    mapping:
      <match>: <replacement>
      ...
```
#### Parameters:
- column: str - The column name to map values.
- default_value: Any (optional) - The default value to fill for unmapped values. If not provided, the unmapped values will be filled with NaN.
- mapping: dict - The dictionary mapping the original values to new values.
  - match: str - The value to match.
  - replacement: str - The new value to replace with.
#### Example:
```
- map_value:
    column: City_new
    default_value: Unknown
    mapping:
      New York: NY
      Los Angeles: LA
      Chicago: CHI
```
---

### convert_case
This function converts the case of values in specified columns.


#### Syntax:
``` 
- convert_case:
    mapping:
      <column>: <case_type>
      ...
```
#### Parameters:
- mapping: dict - The dictionary specifying the column names and the desired case type. The case types can be 'uppercase', 'lowercase', 'titlecase', or 'sentencecase'.
  - column: column of which value to convert
  - case_type: lowercase | uppercase | titlecase | sentencecase
#### Example:
```
- convert_case:
    mapping:
      Name_1: uppercase
      Name_2: titlecase
```
---
### rename
This function renames the columns of the DataFrame.


#### Syntax:
```
- rename:
    mapping:
      <column>: <new_column_name>
      ...
```
#### Parameters:
- mapping: dict - The dictionary specifying the column name mappings.
  - column: current name
  - new_column_name: new name
#### Example:
```
- rename:
    mapping:
      Name_2: Last_Name
      Name_1: First_Name
```
---
### sort
This function sorts the DataFrame based on one or more columns.


#### Syntax:
```
- sort:
    mapping:
      <column>: <ascending?>
      ... 
```
#### Parameters:
- mapping: dict - The dictionary specifying the column names as keys and the sort orders (True for ascending, False for descending) as values.  You can sort mulitple columns.
  - column: column to sort
  - ascending: sort ascending for this column?
#### Example:
```
- sort:
    mapping:
      Age: false
      Name: true
```
 

