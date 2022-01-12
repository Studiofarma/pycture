import re
import functools as ft

class Picture:
    def __init__(self, name, length):
        self.name = name
        self.length = length

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self) -> str:
        return str(self.__dict__)

def read_picture(picture_string):
    picture_string_tokens = [s.strip() for s in  picture_string.split()]
    return Picture(picture_string_tokens[1], picture_len(picture_string_tokens[3]))

def picture_len(picture_definition):
    matches = re.findall(r'v?([\dxz]+)(\(\s*(\d+)\s*\))*', picture_definition)
    if matches is None:
        return 0

    return ft.reduce(lambda acc, match: acc + calculate_len(match), matches, 0)

def calculate_len(match):
    repeted_chars = match[0]
    num_in_parenthesis = match[2]

    length = len(repeted_chars)
    if num_in_parenthesis != '':
        length += int(num_in_parenthesis) - 1

    return length
