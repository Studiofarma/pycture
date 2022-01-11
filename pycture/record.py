from pycture import picture as pyc

class Node:
    def __init__(self, data, *children):
        self.data = data
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
    return Node(
        pyc.Picture('banana', 2),
        Node(pyc.Picture('banana', 2)))
