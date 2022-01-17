import pytest
from pycture import record as pyr
from pycture import picture as pyc
from pycture import structure as pys
from pycture import common

@pytest.mark.parametrize('structure, text_record, expected_csv', [
    (
        pys.Structure('banana', 0, 25,
            pys.Structure('banana.pera', 0, 22,
                pys.Structure('banana.pera.seed', start_at = 0, length = 2),
                pys.Structure('banana.pera.fruit', start_at = 2, length = 20),
                ),
            pys.Structure('banana.mela', start_at = 22, length = 3)
            ),
        """0100000000000000000002003
0400000000000000000005006
        """,
        """banana.pera.seed;banana.pera.fruit;banana.mela
01;00000000000000000002;003
04;00000000000000000005;006
""",
    ),
])
def test_can_provide_the_structure_of_a_record(structure, text_record, expected_csv):
    actual_result = converto_to_csv(structure, text_record)
    assert actual_result == expected_csv
    
def converto_to_csv(structure, text_record):    
    def split_to_csv(line, column_definitions):
        columns_text = [line[column.start_at:column.length + column.start_at] for column in column_definitions]
        return ';'.join(columns_text)
    
    structure_list = structure.traverse_leaves(lambda x: x)
    headers = ';'.join([x.name for x in structure_list])
    lines = [split_to_csv(line, structure_list) for line in text_record.splitlines() if common.is_not_empty(line)]
    
    new_line = '\n'
    return f'{headers}{new_line}{new_line.join(lines)}{new_line}'

