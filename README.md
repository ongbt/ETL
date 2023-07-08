 

# Introduction
ChatGPT: https://chat.openai.com/?model=text-davinci-002-render-sha


---

# Guide
## Transformations
### check_data_type
#### Syntax:
```
- check_data_type:
    mapping:
      <column_name>: <data_type>
      ...
```

#### Parameters:
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
#### Syntax:
```
- check_not_blank:
    columns: [<column_name>, <column_name>, ...]
```
#### Example:
```
- check_not_blank:
    columns: [Name, Age, Phone, City, Address, ZipCode, Sex]
```
---
### copy_columns
#### Syntax:
```
- copy_columns:
    mapping:
      <column_name>: <new_column_name>
      ...
```
#### Parameters:
- column_name: column to copy
- new_column_name: name for the new column 
#### Example:
```
- copy_columns:
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
#### Syntax:
```
- split:
    column: <column_name>
    separator: <separator_text>
```
#### Example:
```
- split:
    column: City
    separator: " "
```
---
### replace
#### Syntax:
```
- replace:
    <column_name>: <new_column_name>
    match_value: <match_value>
    replacement: <replacement_text>
``` 
#### Example:
```
- replace:
    column: Phone_new
    match_value: "555"
    replacement: "XXX"

```
---
### replace_text
#### Syntax:
```
- replace_text:
    column: <column_name>
    start_position: <start_position>
    end_position: <end_position>
    replacement: <replacement_text>
    start: True | False
```
#### Parameters:
- start_position: zero-based position
- end_position: zero-based position
- start: start from the begining of the text?

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
#### Syntax:
``` 
- merge:
    columns: [<column_name>, <column_name>]
    separator: <separator_text>
    output_column: <column_name>
```
#### Example:
```
- merge:
    columns: [Address, City]
    separator: ", "
    output_column: "Address and City"
```
---
### filter_records
#### Syntax:
```
- filter_records:
    condition: <condition>
```
#### Parameters:
- condition: TODO

#### Example:
```
- filter_records:
    condition: "(Age <= 30) and (ZipCode >= 50000)"
```
---
### map_value
``` 
- map_value:
    column: <column_name>
    default_value: <default_value>
    mapping:
      <source_value>: <replacement_value>
      ...
```
#### Parameters:
- default_value: value to be used as the replacement value if no match is found for the source_value
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
### split_pair
#### Syntax:
```
- split_pair:
    column: <column_name>
    separator: <separator_text>
    first:  True | False
```
#### Parameters:
- separator: separator text
- first: spilt at the first occurrence of the separator in the text? If false, it will split at the last occurrence
#### Example:
```
- split_pair:
    column: Name
    separator: " "
    first: false
```
---
### convert_case
#### Syntax:
``` 
- convert_case:
    mapping:
      <column_name>: <case_type>
      ...
```
#### Parameters:
- column_name: column of which value to convert
- case_type: lowercase | uppercase | titlecase | sentencecase
#### Example:
```
- convert_case:
    mapping:
      Name_1: uppercase
      Name_2: titlecase
```
---
### rename_column
#### Syntax:
```
- rename_column:
    mapping:
      <column_name>: <new_column_name>
      ...
```
#### Parameters:
- column_name: current name
- new_column_name: new name
#### Example:
```
- rename_column:
    mapping:
      Name_2: Last_Name
      Name_1: First_Name
```
---
### sort
#### Syntax:
```
- sort:
    mapping:
      <column_name>: <ascending?>
      ... 
```
#### Parameters:
- ascending: sort ascending for this column_name?
#### Example:
```
- sort:
    mapping:
      Age: false
      Name: true
```
 

