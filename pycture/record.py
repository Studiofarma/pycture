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

    def __eq__(self, other):
        return common.eq(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.__dict__)

def read_record(picture_definition):
    lines = picture_definition.split('.')
    interpreted_lines = [pyc.read_picture(l) for l in lines if is_not_empty(l.strip())]

    record = interpreted_lines[0]
    for line in interpreted_lines[1:]:
        record.add(line)

    return record

def is_not_empty(string):
    return string != ''
