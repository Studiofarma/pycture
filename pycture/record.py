from pycture import picture as pyc
from pycture import common

class Record:
    def __init__(self, name, *children):
        self.data = name
        self.children = list(children)

    def __eq__(self, other):
        return common.eq(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self) -> str:
        return str(self.__dict__)

def read_record(picture_definition):
    lines = picture_definition.split('.')
    lines_by_tokens = [l.split() for l in lines]

    return Record('pera', pyc.Picture('banana', 2))
