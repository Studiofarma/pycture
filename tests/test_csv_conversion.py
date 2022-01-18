import pytest
from pycture import structure as pys
from pycture import conversion
from pycture import common

@pytest.mark.parametrize('structure, text_record, expected_csv, aggregate_by', [
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
""", []
    ),
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
        """banana.pera;banana.mela
0100000000000000000002;003
0400000000000000000005;006
""", ['banana.pera']
    ),
])
def test_can_convert_a_text_to_csv(structure, text_record, expected_csv, aggregate_by):
    actual_result = conversion.converto_to_csv(structure, text_record, aggregate_by)
    assert actual_result == expected_csv

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
"""
    ),
])
def test_can_convert_an_iterator_to_csv(structure, text_record, expected_csv):
    text_record_iterator = _lines_to_iterator(text_record)
    expected_csv_iterator = _lines_to_iterator(expected_csv)

    actual_result_iterator = conversion.convert_iterator_to_csv(structure, text_record_iterator)
    assert list(actual_result_iterator) == list(expected_csv_iterator)

def _lines_to_iterator(lines):
    return (l for l in lines.split('\n') if common.is_not_empty(l))
