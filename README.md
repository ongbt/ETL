 

This user guide provides an overview of the data transformation program and explains how to use each transformation function. The program is designed to perform various data transformations on a Pandas DataFrame.
# Introduction
ChatGPT: https://chat.openai.com/?model=text-davinci-002-render-sha

The data transformation program provides a collection of functions to manipulate and transform data in a Pandas DataFrame. These functions allow you to split, replace, merge, filter, rename, map values, convert case, copy columns, sort, and perform data type and blank value checks.


---

# Guide
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
### filter
This function filters the table to include only the specified columns.




#### Syntax:
```
- filter:
    columns: [<column>, <column>, ...]
```
#### Parameters:
- columns: list - The list of column names to include in the filtered DataFrame.

#### Example:
```
- filter:
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
 

