import pytest
from pycture import structure as pys
from pycture import conversion
from pycture import common
from pycture import filters as pyf

@pytest.mark.parametrize('structure, text_record, expected_csv, aggregate_by, keep_list', [
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
""", [], []
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
        """banana.pera.fruit;banana.mela
00000000000000000002;003
00000000000000000005;006
""", [], ['banana.pera.fruit', 'banana.mela']
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
""", ['banana.pera'], []
    ),
])
def test_can_convert_a_text_to_csv(structure, text_record, expected_csv, aggregate_by, keep_list):
    actual_result = conversion.converto_to_csv(structure, text_record, aggregate_by, keep_list)
    assert actual_result == expected_csv

@pytest.mark.parametrize('structure, text_record, expected_csv, filter_operator', [
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
0100000000000000000002004
        """,
        """banana.pera.seed;banana.pera.fruit;banana.mela
01;00000000000000000002;003
01;00000000000000000002;004
""", pyf.EqualsFilter('banana.pera.seed', '01')
    ),
])
def test_can_convert_a_text_to_csv_filtering_by_operators(structure, text_record, expected_csv, filter_operator):
    actual_result = conversion.converto_to_csv(structure, text_record, filters=filter_operator)
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
