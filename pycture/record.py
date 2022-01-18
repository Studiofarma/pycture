import itertools as it
from functools import cached_property
from pycture import picture as pyc
from pycture import structure as pys
from pycture import common

NEW_LINE = '\n'

class Record:
    def __init__(self, name, level, *children):
        self.name = name
        self.level = level
        self.children = list(children)

    def add(self, child):
        def last_children():
            return self.children[-1]

        if not self.children or \
            isinstance(last_children(), pyc.Picture) or \
            last_children().level == child.level:

            return self._with_child(self.children + [child])
        else:
            return self._with_child(self.children[:-1] + [last_children().add(child)])

    def _with_child(self, children):
        return Record(self.name, self.level, *(children))

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

def read_record(picture_definition):
    picture_definition_without_comments = remove_all_comments_lines(picture_definition)
    
    pictures = filter(
        common.is_not_empty,
        map(clean_comments, picture_definition_without_comments.split('.')))
    pictures = it.dropwhile(lambda p: not is_a_root_variable(p), pictures)
    interpreted_lines = [pyc.read_picture(picture) for picture in pictures]

    record = interpreted_lines[0]
    for line in interpreted_lines[1:]:
        record = record.add(line)

    return record

def remove_all_comments_lines(picture_definition):
    return NEW_LINE.join(
        [p for p in picture_definition.split(NEW_LINE) if not is_a_comment_line(p)])

def clean_comments(picture):
    no_comments = [token for token in picture.split(NEW_LINE) if not should_be_skipped(token)]
    return ''.join(no_comments)

def first_char_is(string, char):
    return string.strip().startswith(char)

def is_a_comment_line(token):
    return len(token) >= 7 and token[6] == '*'

def should_be_skipped(token):
    return first_char_is(token, '|')

def is_a_root_variable(picture):
    cleaned_picture = picture.strip()
    return cleaned_picture.startswith('01') or cleaned_picture.startswith('77')
