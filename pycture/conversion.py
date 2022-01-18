from pycture import common
from pycture import record as pyr

def converto_file_to_csv(definition_filename, text_record_filename, aggregate_by = [], separator=';', new_line = '\n'):
    with open(definition_filename, 'r', encoding='utf-8') as definition_file:
        definition_file_text = definition_file.read()
        record = pyr.read_record(definition_file_text)
        with open(text_record_filename, 'r', encoding='utf-8') as record_file:
            text_record = record_file.read()

            record_structure = record.structure
            return converto_to_csv(record_structure, text_record, aggregate_by, separator, new_line)

def converto_to_csv(structure, text_record, aggregate_by = [], separator=';', new_line = '\n'):
    column_definitions = structure.traverse_leaves(pruned_branches=aggregate_by)
    headers = separator.join([x.name for x in column_definitions])
    lines = [_split_by_column_length(line, column_definitions, separator)
             for line in text_record.splitlines()
             if common.is_not_empty(line)]

    return f'{headers}{new_line}{new_line.join(lines)}{new_line}'


def _split_by_column_length(
    line,
    column_definitions,
    separator,
    row_listner_fn = lambda input_line, output_line: output_line):
    columns_text = [line[column.start_at:column.length + column.start_at]
                    for column in column_definitions]
    csv_row = separator.join(columns_text)
    return row_listner_fn(line, csv_row)
