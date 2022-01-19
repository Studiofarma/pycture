import re
import functools as ft
from functools import cached_property
from pycture import common
from pycture import record as pyr
from pycture import structure as pys

REDEFINES_CONST = 'redefines'

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

    def add_to(self, record):
        return record.add_child(self)

    def __eq__(self, other):
        return common.eq(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.__dict__)

class RedefinesFactory():
    def __init__(self, picture):
        self.picture = picture
        self.level = picture.level

    def add_to(self, record):
        last_children = record.last_children()
        if isinstance(last_children, pyr.Redefines):
            redefines = last_children.add_redefinition(self.picture)
        else:
            redefines = pyr.Redefines(last_children, self.picture)

        return record.with_last_children(redefines)

def read_picture(picture_string, ignore_prefix = ''):
    picture_string_tokens = [s.strip() for s in picture_string.split()]
    start_index = _max_index_of_numeric(picture_string_tokens[:2], 1)
    level = int(picture_string_tokens[start_index])
    name_index = start_index + 1
    name = remove_prefix(picture_string_tokens[name_index], ignore_prefix)

    is_redefines = _is_redefines(picture_string_tokens, name_index)
    picture_string_tokens = _remove_redefines_keywords(picture_string_tokens, name, is_redefines)

    if len(picture_string_tokens) == 2 + start_index:
        my_return = pyr.Record(name, level)
    else:
        my_return = Picture(
            name = name,
            length = picture_len(picture_string_tokens[start_index + 3]),
            level = level)

    if is_redefines:
        my_return = RedefinesFactory(my_return)

    return my_return

def _remove_redefines_keywords(picture_string_tokens, name, is_redefines):
    return [t for t in picture_string_tokens 
            if t not in (REDEFINES_CONST, name) or not is_redefines]

def _is_redefines(picture_string_tokens, name_index):
    redefines_index = name_index + 1
    if len(picture_string_tokens) > redefines_index:
        return picture_string_tokens[redefines_index] == REDEFINES_CONST
    else:
        return False

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
