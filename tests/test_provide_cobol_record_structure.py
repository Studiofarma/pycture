import pytest
from pycture import record as pyr
from pycture import picture as pyc
from pycture import structure as pys

@pytest.mark.parametrize('record, expected_result', [
    (
        pyc.Picture('pera', 2, level=1),
        pys.Structure('pera', start_at = 0)
    ),
    (
        pyr.Record('banana', 1, pyc.Picture('pera', 2, 2)),
        pys.Structure('banana', 0,
            pys.Structure('banana.pera', start_at = 0))
    ),
    (
        pyr.Record('banana', 1,
            pyc.Picture('pera', length = 2, level = 2),
            pyc.Picture('mela', length = 3, level = 2)),
        pys.Structure('banana', 0,
            pys.Structure('banana.pera', start_at = 0),
            pys.Structure('banana.mela', start_at = 2)
            )
    ),
])
def test_can_convert_a_cobol_picture_to_a_python_dictonary(record, expected_result):
    actual_result = pys.read_structure(record)
    assert actual_result == expected_result
