from pycture import picture as pyc

class Record:
    def __init__(self, name, *children):
        self.data = name
        self.children = list(children)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self) -> str:
        return str(self.__dict__)

def read_record(picture_definition):
    lines = picture_definition.split('.')
    lines_by_tokens = [l.split() for l in lines]

    return Record('pera', pyc.Picture('banana', 2))
