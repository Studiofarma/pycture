import re
import functools as ft
from pycture import common
from pycture import record as pyr

class Picture:
    def __init__(self, name, length, level = 77):
        self.level = level
        self.name = name
        self.length = length

    def __eq__(self, other):
        return common.eq(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.__dict__)

def read_picture(picture_string):
    picture_string_tokens = [s.strip() for s in  picture_string.split()]
    level = int(picture_string_tokens[0])

    if len(picture_string_tokens) == 2:
        return pyr.Record(picture_string_tokens[1], level)

    return Picture(
        picture_string_tokens[1],
        picture_len(picture_string_tokens[3]),
        level)

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
