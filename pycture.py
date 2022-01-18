#!/usr/bin/python

import argparse
from tqdm import tqdm
from pycture import conversion
from pycture import record as pyr

def main(args):
    data_filename = args.data_filename
    definition_filename = args.definition_filename
    output_filename = args.output if args.output is not None else "out.csv"

    definition_file_text = read_file(definition_filename)

    with open(data_filename, 'r', encoding='utf-8') as datafile_iterator:
        record = pyr.read_record(definition_file_text)
        record_structure = record.structure

        if args.verbose:
            print(record_structure)

        data_lines = count_file_lines(data_filename)
        with tqdm(total=data_lines) as progress_bar:
            def update_bar(i, _, line_out):
                progress_bar.set_description(f'Processed line {i}')
                progress_bar.update()
                return line_out

            csv_text_iterator = conversion.convert_iterator_to_csv(
                record_structure, 
                datafile_iterator,
                row_listner_fn = update_bar)

            write_to_output(output_filename, csv_text_iterator)

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_to_output(output_filename, csv_text):
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        output_file.write(csv_text)

def count_file_lines(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return len(list(f))

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
    parser.add_argument(
        '-v', '--verbose',  action='store_true',
        help='display more parsing informations, like the interpreted Cobol picture')
    args = parser.parse_args()

    try:
        main(args)
    except Exception as e:
        print(e)
        parser.print_help()
