import itertools
from pycturelib import common
from pycturelib import record as pyr
from pycturelib import filters as pyf

def _row_identity(i, input_line, output_line):
    return output_line

def converto_file_to_csv(
    definition_filename,
    text_record_filename,
    aggregate_by = [],
    separator=';',
    new_line = '\n',
    row_listner_fn = _row_identity):
    with open(definition_filename, 'r', encoding='utf-8') as definition_file:
        definition_file_text = definition_file.read()
        record = pyr.read_record(definition_file_text)
        with open(text_record_filename, 'r', encoding='utf-8') as record_file:
            text_record = record_file.read()

            record_structure = record.structure
            return converto_to_csv(
                record_structure,
                text_record,
                aggregate_by,
                separator,
                new_line,
                row_listner_fn)

def converto_to_csv(
    structure,
    text_record,
    aggregate_by = [],
    keep_list = [],
    filters = pyf.MatchAllFilter(),
    separator=';',
    new_line = '\n',
    row_listner_fn = _row_identity):

    text_record_iterator = (record for record in text_record.splitlines())
    csv_lines_iterator = convert_iterator_to_csv(
        structure,
        text_record_iterator,
        aggregate_by,
        keep_list,
        filters,
        separator,
        row_listner_fn)

    return f'{new_line.join(csv_lines_iterator)}{new_line}'

def convert_iterator_to_csv(
    structure,
    text_record_iterator,
    aggregate_by = [],
    keep_list = [],
    filters = pyf.MatchAllFilter(),
    separator=';',
    row_listner_fn = _row_identity,
    write_headers=True):
    column_definitions = structure.traverse_leaves(
        pruned_branches=aggregate_by,
        keep_branches=keep_list)

    headers = separator.join([x.name for x in column_definitions])
    cached_filter = filters.with_columns(column_definitions)

    lines_iterator = map(
        lambda iline: _split_by_column_length(iline[0], iline[1], column_definitions, separator, row_listner_fn),
        filter(
            lambda iline: common.is_not_empty(iline[1]) and cached_filter.match(iline[1]),
            enumerate(text_record_iterator)))

    return itertools.chain([headers], lines_iterator) if write_headers else lines_iterator

def _split_by_column_length(
    i,
    line,
    column_definitions,
    separator,
    row_listner_fn):
    columns_text = [line[column.start_at:column.length + column.start_at]
                    for column in column_definitions]
    csv_row = separator.join(columns_text)
    csv_row = csv_row.replace('\n', ' ')
    return row_listner_fn(i, line, csv_row)
