from pycture import common
from pycture import record as pyr

class Structure:
    def __init__(self, name, start_at, *childred_structures):
        self.name = name
        self.start_at = start_at
        self.childred_structures = list(childred_structures)

    def add(self, children):
        current_length = 0
        for child in children:
            structure = Structure(f'{self.name}.{child.name}', current_length)
            if isinstance(child, pyr.Record):
                structure.add(child.children)

            current_length += child.size
            self.childred_structures.append(structure)

    def __eq__(self, other):
        return common.eq(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.__dict__)

def read_structure(record):
    root = Structure(record.name, 0)
    if isinstance(record, pyr.Record):
        root.add(record.children)
    return root
