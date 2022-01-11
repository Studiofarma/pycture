import pytest
from pycture import picture as pyc

@pytest.mark.parametrize('picture, expected_result', [
    ('77 banana pic 9', pyc.Picture('banana', 1)),
    ('77 banana pic 99', pyc.Picture('banana', 2)),
    ('77     banana   pic    99', pyc.Picture('banana', 2)),
    (' 77 banana   pic    99   ', pyc.Picture('banana', 2)),
    (' 77 banana   pic    9(02)   ', pyc.Picture('banana', 2)),
    (' 01 pera   pic    9(03)v9(2)   ', pyc.Picture('pera', 5)),
])
def test_can_convert_a_cobol_picture_to_a_picture_object(picture, expected_result):
    actual_result = pyc.read_picture(picture)
    assert actual_result == expected_result

@pytest.mark.parametrize('picture_definition, expected_result', [
    ['9', 1],
    ['99', 2],
    ['9(02)', 2],
    ['9( 03 )', 3],
    ['9( 03)', 3],
    ['9(00003)', 3],
    ['9(3)', 3],
    ['99(3)', 4],
    ['xxxx', 4],
    ['xxx9', 4],
    ['x(2)', 2],
    ['z(2)', 2],
    ['xx(2)', 3],
    ['9(2)v9', 3],
    ['9(2)v99(02)', 5],
    ['9(2)v9(040)', 42],
])
def test_can_parse_the_length_of_a_picture(picture_definition, expected_result):
    actual_result = pyc.picture_len(picture_definition)
    assert actual_result == expected_result
