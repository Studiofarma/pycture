import pytest
from pycture import record as pyr
from pycture import picture as pyc

@pytest.mark.parametrize('record, expected_result', [
    (
        '01 banana. 02 pera pic 9(2).',
        pyr.Record('banana', 1, pyc.Picture('pera', 2, 2))
    )
])
def test_can_convert_a_cobol_picture_to_a_python_dictonary(record, expected_result):
    actual_result = pyr.read_record(record)
    assert actual_result == expected_result
