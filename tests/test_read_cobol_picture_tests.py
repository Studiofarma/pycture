import pytest

@pytest.mark.parametrize('picture, expected_result', [
    ('77 banana pic 9', { 'banana': 1 }),
    ('77 banana pic 99', { 'banana': 2 }),
    ('77     banana   pic    99', { 'banana': 2 }),
    (' 77 banana   pic    99   ', { 'banana': 2 }),
])
def test_can_convert_a_cobol_picture_to_a_python_dictonary(picture, expected_result):
    actual_result = read_picture(picture)
    assert actual_result == expected_result


def read_picture(picture_string):
    picture_string_tokens = list(map(lambda s: s.strip(), picture_string.split()))
    return { picture_string_tokens[1]: len(picture_string_tokens[3]) }
