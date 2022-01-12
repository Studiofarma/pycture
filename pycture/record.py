from pycture import picture as pyc
from pycture import common

class Record:
    def __init__(self, name, level, *children):
        self.name = name
        self.level = level
        self.children = list(children)

    def add(self, child):
        self.children.append(child)

    def __eq__(self, other):
        return common.eq(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self) -> str:
        return str(self.__dict__)

def read_record(picture_definition):
    lines = picture_definition.split('.')
    interpreted_lines = [pyc.read_picture(l) for l in lines if l]

    record = interpreted_lines[0]
    record.add(interpreted_lines[1])

    return record
