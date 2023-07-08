# ETL


# Introduction
ChatGPT: https://chat.openai.com/?model=text-davinci-002-render-sha


---

# Guide
## Transformations
### check_data_type
```
- check_data_type:
    mapping:
      <column_name>: <data_type>
      ...
```

data_type options: object | int64 | datetime64
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
```
- copy_columns:
    mapping:
      <column_name>: <new_column_name>
      ...
```
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
```
- replace_text:
    column: <column_name>
    start_position: <start_position>
    end_position: <end_position>
    replacement: <replacement_text>
    start: <start_from_begining?>
```
start_position: zero-based position
end_position: zero-based position

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
```
- filter_records:
    condition: <condition>
```
condition: e.g. "(Age <= 30) and (ZipCode >= 50000)"

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
```
- split_pair:
    column: <column_name>
    separator: <separator>
    first: <first_occurrence?>
```
#### Example:
```
- split_pair:
    column: Name
    separator: " "
    first: false
```
---
### convert_case
``` 
- convert_case:
    mapping:
      <column_name>: <case_type>
      ...
```
case_type: lowercase | uppercase | titlecase | sentencecase
#### Example:
```
- convert_case:
    mapping:
      Name_1: uppercase
      Name_2: titlecase
```
---
### rename_column
```
- rename_column:
    mapping:
      <column_name>: <new_column_name>
      ...
```
#### Example:
```
- rename_column:
    mapping:
      Name_2: Last_Name
      Name_1: First_Name
```
---
### sort
```
- sort:
    mapping:
      <column_name>: <ascending?>
      ... 
```
#### Example:
```
- sort:
    mapping:
      Age: false
      Name: true
```
 

