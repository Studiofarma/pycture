from pycture import picture as pyc
import pytest

@pytest.mark.parametrize('picture, expected_result', [
    ('77 banana pic 9', pyc.Picture('banana', 1)),
    ('77 banana pic 99', pyc.Picture('banana', 2)),
    ('77     banana   pic    99', pyc.Picture('banana', 2)),
    (' 77 banana   pic    99   ', pyc.Picture('banana', 2)),
    # (' 77 banana   pic    9(02)   ', pyc.Picture('banana', 2)),
])
def test_can_convert_a_cobol_picture_to_a_python_dictonary(picture, expected_result):
    actual_result = pyc.read_picture(picture)
    assert actual_result == expected_result

@pytest.mark.parametrize('picture_definition, expected_result', [
    ['9', 1],
    ['99', 2],
    # ['9(02)', 2],
])
def test_can_parse_the_length_of_a_picture(picture_definition, expected_result):
    actual_result = pyc.picture_len(picture_definition)
    assert actual_result == expected_result
