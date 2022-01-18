from pycture import common

def converto_to_csv(structure, text_record, separator=';', new_line = '\n'):
    column_definitions = structure.traverse_leaves()
    headers = separator.join([x.name for x in column_definitions])
    lines = [_split_by_column_length(line, column_definitions, separator)
             for line in text_record.splitlines()
             if common.is_not_empty(line)]

    return f'{headers}{new_line}{new_line.join(lines)}{new_line}'


def _split_by_column_length(line, column_definitions, separator):
    columns_text = [line[column.start_at:column.length + column.start_at]
                    for column in column_definitions]
    return separator.join(columns_text)
