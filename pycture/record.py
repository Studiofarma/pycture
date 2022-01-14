from pycture import picture as pyc
from pycture import common

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

            self.children.append(child)
        else:
            last_children().add(child)

    def size(self):
        return sum([child.size() for child in self.children])

    def __eq__(self, other):
        return common.eq(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.__dict__)

def read_record(picture_definition):
    pictures = filter(
        is_not_empty,
        map(clean_comments, picture_definition.split('.')))
    interpreted_lines = [pyc.read_picture(picture) for picture in pictures]

    record = interpreted_lines[0]
    for line in interpreted_lines[1:]:
        record.add(line)

    return record

def clean_comments(picture):
    no_comments = [token for token in picture.split('\n') if not first_char_is(token, '|')]
    return str.join('', no_comments)

def is_not_empty(string):
    return not is_empty(string)

def is_empty(string):
    return string == '' or all(map(lambda c: c == ' ', string))

def first_char_is(string, char):
    return string.strip().startswith(char)
