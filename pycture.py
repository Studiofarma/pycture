#!/usr/bin/python

import argparse
import os
import sys
import fnmatch
from tqdm import tqdm
from pathlib import Path
from pycture import conversion
from pycture import record as pyr

def main(args):
    data_filename = args.data_filename
    definition_filename = args.definition_filename
    output_filename = args.output.strip()

    record_structure = read_record(definition_filename, args.prefix)

    if args.verbose or args.print_definition:
        pretty_print(record_structure)
        if args.print_definition:
            exit(0)

    output_filename = check_output_exist(output_filename)
    convert_all_files(args.aggregate_by, data_filename, output_filename, record_structure)

def check_output_exist(output_filename):
    new_name = rename_if_exist(output_filename)
    while new_name != output_filename:
        new_name = rename_if_exist(new_name)
        output_filename = new_name

    return new_name

def rename_if_exist(output_filename):
    if os.path.exists(output_filename):
        print(f'{output_filename} already exists. Do you want to overwrite it?. If no it will be renamed (Y/n)', end=' ')
        answer = sys.stdin.readline().strip()
        if answer in ('Y', 'y',''):
            os.remove(output_filename)
            return output_filename

        return file_rename(output_filename)

    return output_filename

def file_rename(output_filename):
    directory = os.path.dirname(output_filename)
    basename = os.path.basename(output_filename)
    filename_tokens = basename.split('.')

    renamed = '.'.join([filename_tokens[0], 'renamed'] + filename_tokens[1:])
    return os.path.join(directory, renamed)

def convert_all_files(aggregate_by, data_filename, output_filename, record_structure):
    data_filenames = file_list(data_filename)
    for filename in data_filenames:
        convert(aggregate_by, output_filename, record_structure, filename)

def convert(aggregate_by, output_filename, record_structure, filename):
    with open(filename, 'r', encoding='utf-8') as datafile_iterator:
        data_lines = count_file_lines(filename)
        with tqdm(total=data_lines) as progress_bar:
            def update_bar(i, _, line_out):
                progress_bar.set_description(os.path.basename(filename))
                progress_bar.update()
                return line_out

            csv_text_iterator = conversion.convert_iterator_to_csv(
                        record_structure,
                        datafile_iterator,
                        aggregate_by=aggregate_by,
                        row_listner_fn = update_bar)

            write_to_output(output_filename, csv_text_iterator)

def file_list(path):
    dir_name = os.path.dirname(path)
    pattern = os.path.basename(path)
    out_file_list = []
    for root, _, files in os.walk(dir_name):
        for filename in fnmatch.filter(files, pattern):
            out_file_list.append(os.path.join(root, filename))

    return out_file_list

def read_record(definition_filename, prefix):
    definition_file_text = read_file(definition_filename)
    record = pyr.read_record(definition_file_text, prefix)
    return record.structure

def pretty_print(record_obj):
    import json
    record_dict = json.loads(str(record_obj).replace('\'', "\""))
    json_obj = json.dumps(record_dict, indent=4)
    print(json_obj)

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

def write_to_output(output_filename, csv_text_iterator):
    with open(output_filename, 'a', encoding='utf-8') as output_file:
        output_file.writelines(f'{l}\n' for l in csv_text_iterator)

def count_file_lines(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return len(list(f))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert a serialized Cobol data file into CSV, given the Cobol definition file.')
    parser.add_argument(
        'data_filename', nargs='?',
        help='The filename of the data export in the COBOL format. You can use wildchars like * in order to match many files (es. c:\\mydir\\*.txt)')
    parser.add_argument(
        'definition_filename', nargs='?',
        help='the filename of COBOL picture definition that describes the data')
    parser.add_argument(
        '-o', '--output',  nargs='?', type=str, const='out.csv', default='out.csv',
        help='the filename to give to the output file')
    parser.add_argument(
        '-v', '--verbose',  action='store_true',
        help='display more parsing informations, like the interpreted Cobol picture')
    parser.add_argument(
        '-d', '--debug',  action='store_true',
        help='display some debug informations, like exception stacktrace')
    parser.add_argument(
        '-p', '--print-definition',  action='store_true',
        help='display the json of the parsed Cobol picture')
    parser.add_argument(
        '--prefix',  nargs='?', type=str, const='', default='',
        help='remove a prefix from the name of Cobol variables')
    parser.add_argument(
        '--aggregate-by',  nargs='+', default=[],
        help='variables names used to aggregate')
    args = parser.parse_args()

    try:
        main(args)
    except Exception as e:
        print(e)
        parser.print_help()
        if args.debug:
            raise e
