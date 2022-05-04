# How to use

```
usage: pycture.py [-h] [-o [OUTPUT]] [-vv] [-d] [-p] [--prefix [PREFIX]] [--aggregate-by AGGREGATE_BY [AGGREGATE_BY ...]] [--keep-only KEEP_ONLY [KEEP_ONLY ...]] [--redefines REDEFINES [REDEFINES ...]]
                  [--eq EQ EQ] [--gt GT GT] [--lt LT LT] [--neq NEQ NEQ]
                  [data_filename] [definition_filename]

Convert a serialized Cobol data file into CSV, given the Cobol definition file.

positional arguments:
  data_filename         The filename of the data export in the COBOL format. You can use wildchars like * in order to match many files (es. c:\mydir\*.txt)
  definition_filename   the filename of COBOL picture definition that describes the data

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT], --output [OUTPUT]
                        the filename to give to the output file
  -vv, --verbose        display more parsing informations, like the interpreted Cobol picture
  -d, --debug           display some debug informations, like exception stacktrace
  -p, --print-definition
                        display the json of the parsed Cobol picture
  --prefix [PREFIX]     remove a prefix from the name of Cobol variables
  --aggregate-by AGGREGATE_BY [AGGREGATE_BY ...]
                        variables names used to aggregate
  --keep-only KEEP_ONLY [KEEP_ONLY ...]
                        you can pass a limited list of variables to export
  --redefines REDEFINES [REDEFINES ...]
                        the list of redefines to use
  --eq EQ EQ            filter record by equality. Example: --eq variable-name xx
  --gt GT GT            filter record by greater then. Example: --gt variable-name xx
  --lt LT LT            filter record by less then. Example: --lt variable-name xx
  --neq NEQ NEQ         filter record by not equals. Example: --neq variable-name xx
```