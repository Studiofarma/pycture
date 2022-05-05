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
 - cd into into
 - install requirements
 - run the script with `python pycture.py [path/to/definition/filename] [path/to/data/filename]`
 - run the script with `python pycture.py -h` for help

## How it works

Pycture parses the file definition and creates an internal representation of it. 

Pycture then uses this representation to print the headers of the CSV and split all the contigous record column, into CSV columns.

### Example

Given the following picture definition

`example/mydefinition.cpy`

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
python pycture.py example/mydefinition.cpy -p
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

Given the following data file

`example/mydata.txt`

```
luca                          piccinelli                    19850316
paolo                         venturi                       19911216
```

Running

```
python pycture.py example/mydefinition.cpy example/mydata.txt -o example/out.csv
```

will output

`example/out.csv`

```cvs
person.firstname;person.lastname;person.date-of-birth.date-of-birth-year;person.date-of-birth.date-of-birth-month;person.date-of-birth.date-of-birth-day
luca                          ;piccinelli                    ;1985;03;16
paolo                         ;venturi                       ;1991;12;16
```

## Help `python pycture.py -h`

```
usage: pycture.py [-h] [-o [OUTPUT]] [-vv] [-d] [-p] [--prefix [PREFIX]] [--use-groups USE_GROUPS [USE_GROUPS ...]] [--keep-only KEEP_ONLY [KEEP_ONLY ...]] [--redefines REDEFINES [REDEFINES ...]] [--eq EQ EQ]
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