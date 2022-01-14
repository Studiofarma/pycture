from pycture import common
from pycture import record as pyr

class Structure:
    def __init__(self, name, start_at, length, *childred_structures):
        self.name = name
        self.start_at = start_at
        self.length = length
        self.childred_structures = list(childred_structures)

    def add(self, children):
        current_position = 0
        for child in children:
            structure = Structure(f'{self.name}.{child.name}', current_position, child.size)
            if isinstance(child, pyr.Record):
                structure.add(child.children)

            current_position += child.size
            self.childred_structures.append(structure)

    def __eq__(self, other):
        return common.eq(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.__dict__)

def read_structure(record):
    root = Structure(record.name, 0, record.size)
    if isinstance(record, pyr.Record):
        root.add(record.children)
    return root
