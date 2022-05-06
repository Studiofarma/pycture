import itertools as it
from functools import cached_property
from pycturelib import picture as pyc
from pycturelib import structure as pys
from pycturelib import common

NEW_LINE = '\n'

class Record:
    def __init__(self, name, level, *children):
        self.name = name
        self.level = level
        self.children = list(children)

    def add(self, child):
        if not self.children or self.last_children().level == child.level:
            return child.add_to(self)

        return self.with_last_children(self.last_children().add(child))

    def with_last_children(self, child):
        return self.with_child(self.children[:-1] + [child])

    def add_to(self, record):
        return record.add_child(self)

    def add_child(self, child):
        return self.with_child(self.children + [child])

    def last_children(self):
        return self.children[-1]

    def with_child(self, children):
        return Record(self.name, self.level, *(children))

    def redefines(self, redefines_list):
        return self.with_child([child.redefines(redefines_list) for child in self.children])

    @cached_property
    def size(self):
        return sum([child.size for child in self.children])

    @cached_property
    def structure(self):
        return pys.read_structure(self)

    def __eq__(self, other):
        return common.eq(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.__dict__)

class Redefines:
    def __init__(self, original_definition, *redefinitions):
        self.original_definition = original_definition
        self.level = original_definition.level
        self.size = original_definition.size
        self.redefinitions = list(redefinitions)

    @property
    def name(self):
        return self.original_definition.name

    def choosen_definition(self):
        return self.original_definition

    def add(self, element):
        if element.level == self.level:
            return self.add_redefinition(element)
        return self.with_last_redefinition(self.last_redefinition().add(element))

    def with_last_redefinition(self, redefinition):
        return self.with_redefinitions(self.redefinitions[:-1] + [redefinition])

    def add_redefinition(self, redefinition):
        return self.with_redefinitions(self.redefinitions + [redefinition])

    def with_redefinitions(self, redefinitions):
        return Redefines(self.original_definition, *(redefinitions))

    def last_redefinition(self):
        return self.redefinitions[-1]

    def redefines(self, redefines_list):
        redefine = next((r for r in self.redefinitions if r.name in redefines_list), None)
        return self.original_definition if redefine is None else redefine

    def __eq__(self, other):
        return common.eq(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.__dict__)

def read_record(picture_definition, ignore_prefix=''):
    picture_definition_without_comments = remove_all_comments_lines(picture_definition)

    pictures = filter(
        common.is_not_empty,
        map(remove_newlines, picture_definition_without_comments.split('.')))
    pictures = it.dropwhile(lambda p: not is_a_root_variable(p), pictures)
    interpreted_lines = [pyc.read_picture(picture, ignore_prefix) for picture in pictures]

    record = interpreted_lines[0]
    for line in interpreted_lines[1:]:
        record = record.add(line)

    return record

def remove_all_comments_lines(picture_definition):
    return NEW_LINE.join(
        [remove_bar_comments(p) \
            for p in picture_definition.split(NEW_LINE) \
            if not is_a_comment_line(p)]
    )

def remove_newlines(picture):
    return picture.replace(NEW_LINE, '')

def remove_bar_comments(token):
    try:
        return token[:token.index('|')]
    except ValueError:
        return token

def first_char_is(string, char):
    return string.strip().startswith(char)

def is_a_comment_line(token):
    return len(token) >= 7 and token[6] == '*'

def should_be_skipped(token):
    return first_char_is(token, '|')

def is_a_root_variable(picture):
    cleaned_picture = picture.strip()
    return cleaned_picture.startswith('01') or cleaned_picture.startswith('77')
