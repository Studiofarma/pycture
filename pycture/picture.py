import re
import functools as ft
from pycture import common
from pycture import record as pyr

class Picture:
    def __init__(self, name, length, level = 77):
        self.level = level
        self.name = name
        self.length = length

    def size(self):
        return self.length

    def __eq__(self, other):
        return common.eq(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.__dict__)

def read_picture(picture_string, ignore_prefix = ''):
    picture_string_tokens = [s.strip() for s in  picture_string.split()]
    level = int(picture_string_tokens[0])
    name = remove_prefix(picture_string_tokens[1], ignore_prefix)
    
    if len(picture_string_tokens) == 2:
        return pyr.Record(name, level)

    return Picture(
        name = name,
        length = picture_len(picture_string_tokens[3]),
        level = level)

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

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
