import re
import functools as ft
from functools import cached_property
from pycture import common
from pycture import record as pyr
from pycture import structure as pys

class Picture:
    def __init__(self, name, length, level = 77):
        self.level = level
        self.name = name
        self.length = length

    @property
    def size(self):
        return self.length

    @cached_property
    def structure(self):
        return pys.read_structure(self)

    def __eq__(self, other):
        return common.eq(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.__dict__)

def read_picture(picture_string, ignore_prefix = ''):
    picture_string_tokens = [s.strip() for s in  picture_string.split()]
    start_index = _max_index_of_numeric(picture_string_tokens[:2], 1)
    level = int(picture_string_tokens[start_index])
    name = remove_prefix(picture_string_tokens[start_index + 1], ignore_prefix)

    if len(picture_string_tokens) == 2 + start_index:
        return pyr.Record(name, level)

    return Picture(
        name = name,
        length = picture_len(picture_string_tokens[start_index + 3]),
        level = level)

def _max_index_of_numeric(tokens, max_index):
    return min(_max_index_of(tokens, lambda x: x.isnumeric()), max_index)

def _max_index_of(l, filter_fn=lambda x: True):
    return max(filter(lambda x: filter_fn(x[1]), enumerate(l)), key=lambda x: x[0])[0]

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
    repeated_chars = match[0]
    num_in_parenthesis = match[2]

    length = len(repeated_chars)
    if num_in_parenthesis != '':
        length += int(num_in_parenthesis) - 1

    return length
