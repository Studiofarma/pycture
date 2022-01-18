#!/usr/bin/python

import argparse
from tqdm import trange
from time import sleep
from pycture import conversion

def main(args):
    data_filename = args.data_filename
    definition_filename = args.definition_filename
    output_filename = args.output if args.output is not None else "out.csv"

    csv_text = conversion.converto_file_to_csv(definition_filename, data_filename)

    with open(output_filename, 'w', encoding='utf-8') as output_file:
        output_file.write(csv_text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description='Convert a serialized Cobol data file into CSV, given the Cobol definition file.')
    parser.add_argument(
        'data_filename', nargs='?',
        help='the filename of the data export in the COBOL format')
    parser.add_argument(
        'definition_filename', nargs='?',
        help='the filename of COBOL picture definition that describes the data')
    parser.add_argument(
        '-o', '--output',  nargs='?',
        help='the filename to give to the output file')
    args = parser.parse_args()

    main(args)
