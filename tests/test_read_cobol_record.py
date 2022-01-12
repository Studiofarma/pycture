import pytest
from pycture import record as pyr
from pycture import picture as pyc

@pytest.mark.parametrize('record, expected_result', [
    (
        '01 banana. 02 pera pic 9(2).',
        pyr.Record('banana', 1, pyc.Picture('pera', 2, 2))
    ),
    (
        """01 banana.
                02 pera pic 9(2).
                
        """,
        pyr.Record('banana', 1, pyc.Picture('pera', 2, 2))
    ),
    (
        """01 banana.
                02 pera pic 9(2).
                02 mela pic xxx.
        """,
        pyr.Record('banana', 1,
            pyc.Picture('pera', 2, 2),
            pyc.Picture('mela', 3, 2))
    ),
    (
        """01 banana.
                02 pera.
                    03 seed pic 9(2)
                    03 fruit pic x(20)
                02 mela pic xxx.
        """,
        pyr.Record('banana', 1,
            pyr.Record('pera', 2,
                pyc.Picture('seed', 2, level = 3),
                pyc.Picture('fruit', 20, level = 3)
            ),
            pyc.Picture('mela', 3, level = 2))
    ),
])
def test_can_convert_a_cobol_picture_to_a_python_dictonary(record, expected_result):
    actual_result = pyr.read_record(record)
    assert actual_result == expected_result
