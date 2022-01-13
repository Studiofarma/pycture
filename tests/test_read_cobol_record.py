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
                    03 seed pic 9(2).
                    03 fruit pic x(20).
                02 mela pic xxx.
        """,
        pyr.Record('banana', 1,
            pyr.Record('pera', 2,
                pyc.Picture('seed', 2, level = 3),
                pyc.Picture('fruit', 20, level = 3)
            ),
            pyc.Picture('mela', 3, level = 2))
    ),
    ('77 banana pic 9', pyc.Picture('banana', 1)),
    (' 01 pera   pic    9(03)v9(2)   ', pyc.Picture('pera', 5, 1)),    
    (
        """01 banana.
                02 pera.
                    03 fruit.
                        05 juice pic xx.
                        05 taste pic z(6).
                    03 seed pic 9(2).
                02 mela.
                    03 seed pic 9(2).
                    03 fruit pic x(20).
        """,
        pyr.Record('banana', 1,
            pyr.Record('pera', 2,
                pyr.Record('fruit', 3,
                    pyc.Picture('juice', 2, level = 5),
                    pyc.Picture('taste', 6, level = 5)
                ),
                pyc.Picture('seed', 2, level = 3),
            ),
            pyr.Record('mela', 2,
                pyc.Picture('seed', 2, level = 3),
                pyc.Picture('fruit', 20, level = 3)
            ))
    ),
    (
        """01 banana. | comments
                02 pera pic 9(2).
                02 mela pic xxx.
        """,
        pyr.Record('banana', 1,
            pyc.Picture('pera', 2, 2),
            pyc.Picture('mela', 3, 2))
    ),
    (
        """01 banana. | comments
                | another comment
                02 pera pic 9(2).
                02 mela pic xxx.
        """,
        pyr.Record('banana', 1,
            pyc.Picture('pera', 2, 2),
            pyc.Picture('mela', 3, 2))
    ),
    (
        """01 banana.   | comments 02 arancia pic 9(2).
                02 pera pic 9(2).
                02 mela pic xxx.
        """,
        pyr.Record('banana', 1,
            pyc.Picture('pera', 2, 2),
            pyc.Picture('mela', 3, 2))
    ),
])
def test_can_convert_a_cobol_picture_to_a_python_dictonary(record, expected_result):
    actual_result = pyr.read_record(record)
    assert actual_result == expected_result

@pytest.mark.parametrize('record, expected_result', [
    (pyr.Record('banana', 1, pyc.Picture('pera', 2, 2)), 2),
    (pyr.Record('banana', 1,
        pyc.Picture('pera', 2, 2),
        pyc.Picture('mela', 3, 2)), 5),
    (pyr.Record('banana', 1,
            pyr.Record('pera', 2,
                pyr.Record('fruit', 3,
                    pyc.Picture('juice', 2, level = 5),
                    pyc.Picture('taste', 6, level = 5)
                ),
                pyc.Picture('seed', 2, level = 3),
            ),
            pyr.Record('mela', 2,
                pyc.Picture('seed', 2, level = 3),
                pyc.Picture('fruit', 20, level = 3)
            )), 32)
])
def test_return_the_size_of_the_record(record, expected_result):
    actual_result = record.size()
    assert actual_result == expected_result
