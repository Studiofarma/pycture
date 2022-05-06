# Pycture
Convert a serialized Cobol text data file into CSV, given the Cobol definition file (FD)

## Getting Started

Pycture uses **python 3.9**. (Probably it works also with previos versions of **Python3**)

### Install
```sh
git clone https://github.com/Studiofarma/pycture.git
cd pycture
python -m venv .venv
.\.venv\Scripts\activate (for Windows)
source .venv/bin/activate (for Linux)
pip install -r requirements.txt
```
### Run
```
python pycture.py [path/to/definition/filename] [path/to/data/filename]
```

The above instructions does the following:
 - Clone this repository
 - cd into the correct directory
 - install requirements
 - run the script with `python pycture.py [path/to/definition/filename] [path/to/data/filename]`
 - run the script with `python pycture.py -h` for help



## Help `-h | --help`

```
usage: python pycture.py [-h] [-o [OUTPUT]] [-vv] [-d] [-p] [--prefix [PREFIX]] [--use-groups USE_GROUPS [USE_GROUPS ...]] [--keep-only KEEP_ONLY [KEEP_ONLY ...]] [--redefines REDEFINES [REDEFINES ...]] [--eq EQ EQ]
                  [--gt GT GT] [--lt LT LT] [--neq NEQ NEQ]
                  [definition_filename] [data_filename]

Convert a serialized Cobol data file into CSV, given the Cobol definition file.

positional arguments:
  definition_filename   the filename of COBOL picture definition that describes the data
  data_filename         The filename of the data export in the COBOL format. You can use wildchars like * in order to match many files (es. c:\mydir\*.txt)

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT], --output [OUTPUT]
                        the filename to give to the output file
  -vv, --verbose        display more parsing informations, like the interpreted Cobol picture
  -d, --debug           display some debug informations, like exception stacktrace
  -p, --print-definition
                        display the json of the parsed Cobol picture
  --prefix [PREFIX]     remove a prefix from the name of Cobol variables
  --use-groups USE_GROUPS [USE_GROUPS ...]
                        names of the groups to use
  --keep-only KEEP_ONLY [KEEP_ONLY ...]
                        you can pass a limited list of variables to export
  --redefines REDEFINES [REDEFINES ...]
                        the list of redefines to use
  --eq EQ EQ            filter record by equality. Example: --eq variable-name xx
  --gt GT GT            filter record by greater then. Example: --gt variable-name xx
  --lt LT LT            filter record by less then. Example: --lt variable-name xx
  --neq NEQ NEQ         filter record by not equals. Example: --neq variable-name xx
```

## How it works

Pycture parses the file definition and creates an internal representation of it. 

Pycture then uses the variable names as column headings, and `start_at` and `length` to split all the contiguous record columns, into CSV columns.

## Basic usage and Features Examples

Find example files in [examples](examples).

### Print the definition structure as JSON `-p | --print-definition`

Given the following picture definition

`examples/mydefinition.cpy`

```Cobol
01 person.
    02 firstname pic x(30).
    02 lastname  pic x(30).
    02 date-of-birth.
        03 date-of-birth-year  pic 9(04).
        03 date-of-birth-month pic 9(02).
        03 date-of-birth-day   pic 9(02).
```

we can see the internal representation running 

```sh
python pycture.py examples/mydefinition.cpy -p
```

will print

```json
{
    "name": "person",
    "start_at": 0,
    "length": 68,
    "children_structures": [
        {
            "name": "person.firstname",
            "start_at": 0,
            "length": 30,
            "children_structures": []
        },
        {
            "name": "person.lastname",
            "start_at": 30,
            "length": 30,
            "children_structures": []
        },
        {
            "name": "person.date-of-birth",
            "start_at": 60,
            "length": 8,
            "children_structures": [
                {
                    "name": "person.date-of-birth.date-of-birth-year",
                    "start_at": 60,
                    "length": 4,
                    "children_structures": []
                },
                {
                    "name": "person.date-of-birth.date-of-birth-month",
                    "start_at": 64,
                    "length": 2,
                    "children_structures": []
                },
                {
                    "name": "person.date-of-birth.date-of-birth-day",
                    "start_at": 66,
                    "length": 2,
                    "children_structures": []
                }
            ]
        }
    ]
}

```

### Basic conversion to CSV

Given the following data file

`examples/mydata.txt`

```
luca                          piccinelli                    19850316
paolo                         venturi                       19911216
mario                         rossi                         20000622
```

Running

```
python pycture.py examples/mydefinition.cpy examples/mydata.txt -o examples/out.csv
```

will output

`examples/out.csv`

```csv
person.firstname;person.lastname;person.date-of-birth.date-of-birth-year;person.date-of-birth.date-of-birth-month;person.date-of-birth.date-of-birth-day
luca                          ;piccinelli                    ;1985;03;16
paolo                         ;venturi                       ;1991;12;16
mario                         ;rossi                         ;2000;06;22
```

### Conversion of multiple files to CSV using wildcard characters (e.g. *)

If you have multiple files like [`examples/mydata.txt`](examples/mydata.txt) and [`examples/mydata2.txt`](examples/mydata2.txt)
,match them with `mydata*.txt`

```
python pycture.py examples/mydefinition.cpy "examples/mydata*.txt" -o examples/out-multi.csv
```

`examples/out-multi.csv`

```csv
person.firstname;person.lastname;person.date-of-birth.date-of-birth-year;person.date-of-birth.date-of-birth-month;person.date-of-birth.date-of-birth-day
luca                          ;piccinelli                    ;1985;03;16
paolo                         ;venturi                       ;1991;12;16
mario                         ;rossi                         ;2000;06;22
andrea                        ;bianchi                       ;2001;12;25
sandro                        ;verdi                         ;1960;02;02
```

### Use group names `--use-groups`

In the example above, the group `date-of-birth` is split in 3 column in the CSV. This is because it has 3 subfields.

You can use `--use-groups` and print it as a single column:

```
python pycture.py examples/mydefinition.cpy examples/mydata.txt -o examples/out-group.csv --use-groups person.date-of-birth
```

will output

`examples/out-groups.csv`

```csv
person.firstname;person.lastname;person.date-of-birth
luca                          ;piccinelli                    ;19850316
paolo                         ;venturi                       ;19911216
mario                         ;rossi                         ;20000622
```

If you doubt the name of the group, you can print the JSON definition and watch there the correct name.

### Keep only some column `--keep-only`

You can give the list of the columns to keep:

```
python pycture.py examples/mydefinition.cpy examples/mydata.txt -o examples/out-keep-only.csv --keep-only person.lastname person.date-of-birth.date-of-birth-year
```

will output

`examples/out-keep-only.csv`

```csv
person.lastname;person.date-of-birth.date-of-birth-year
piccinelli                    ;1985
venturi                       ;1991
rossi                         ;2000
```

### Use redefines `--redefines`

Let's consider a definition that redefines a certain field:

`examples/mydefinition-redefines.csv`

```Cobol
01 person.
    02 firstname pic x(30).
    02 lastname  pic x(30).
    02 date-of-birth.
        03 date-of-birth-year  pic 9(04).
        03 date-of-birth-month pic 9(02).
        03 date-of-birth-day   pic 9(02).
    02 date-of-birth-x redefines date-of-birth pic x(08).
```

Pay attention to the last line.

You can choose to use `date-of-birth-x` instead of `date-of-birth` in the internal structure representation.

Lets' display it:

```
 python pycture.py examples/mydefinition-redefines.cpy -p --redefines date-of-birth-x
```

will print

```json
{
    "name": "person",
    "start_at": 0,
    "length": 68,
    "children_structures": [
        {
            "name": "person.firstname",
            "start_at": 0,
            "length": 30,
            "children_structures": []
        },
        {
            "name": "person.lastname",
            "start_at": 30,
            "length": 30,
            "children_structures": []
        },
        {
            "name": "person.date-of-birth-x",
            "start_at": 60,
            "length": 8,
            "children_structures": []
        }
    ]
}
```

### Filter rows `--eq --neq --lt --gt`

There are some basic filters available to filter out rows that doesn't match the given conditions.

Given the following data file

`examples/mydata.txt`

```
luca                          piccinelli                    19850316
paolo                         venturi                       19911216
mario                         rossi                         20000622
```

I want to export only those born after the year 1990

```
python pycture.py examples/mydefinition.cpy examples/mydata.txt -o examples/out-filter.csv --gt person.date-of-birth.date-of-birth-year 1990
```

will output

`examples/out-filter.csv`

```csv
person.firstname;person.lastname;person.date-of-birth.date-of-birth-year;person.date-of-birth.date-of-birth-month;person.date-of-birth.date-of-birth-day
paolo                         ;venturi                       ;1991;12;16
mario                         ;rossi                         ;2000;06;22
```

Filters can be combined in `and`. For example let's export only those born before year 2000 only in the month of march

```
python pycture.py examples/mydefinition.cpy examples/mydata.txt -o examples/out-filter.csv --lt person.date-of-birth.date-of-birth-year 2000 --eq --eq person.date-of-birth.date-of-birth-month 03
```

will output

`examples/out-filter.csv`

```csv
person.firstname;person.lastname;person.date-of-birth.date-of-birth-year;person.date-of-birth.date-of-birth-month;person.date-of-birth.date-of-birth-day
luca                          ;piccinelli                    ;1985;03;16
```

## Files with complex content (comments, multi line pictures etc.)

Refer to these files to have an updated list of the corner cases handled.
 - [tests/test_read_cobol_picture.py](tests/test_read_cobol_picture.py)
 - [tests/test_read_cobol_record.py](tests/test_read_cobol_record.py)

## Known Issues

 - Cobol array tables are not yet parsed, then will have an undefined beaviour.
 - `usage pointer` is not yet handled.