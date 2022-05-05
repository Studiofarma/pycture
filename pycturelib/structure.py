from pycturelib import common
from pycturelib import record as pyr

class Structure:
    def __init__(self, name, start_at, length, *childred_structures):
        self.name = name
        self.start_at = start_at
        self.length = length
        self.children_structures = list(childred_structures)

    def add(self, children, current_position = 0):
        new_childred_structures = []
        for child in children:
            structure = Structure(f'{self.name}.{child.name}', current_position, child.size)
            if isinstance(child, pyr.Record):
                structure = structure.add(child.children, current_position)
            elif isinstance(child, pyr.Redefines):
                choosen_definition = child.choosen_definition()
                if isinstance(choosen_definition, pyr.Record):
                    structure = structure.add(choosen_definition.children, current_position)

            current_position += child.size
            new_childred_structures.append(structure)

        return self._with_child(self.children_structures + new_childred_structures)

    def traverse_leaves(
        self,
        pruned_branches= [],
        keep_branches = [],
        fn = lambda x: x,
        acc = None):

        if acc is None:
            acc = []

        if self.children_structures and self.name not in pruned_branches:
            for child in self.children_structures:
                acc = child.traverse_leaves(pruned_branches, keep_branches, fn, acc)
            return acc

        if not keep_branches or self.name in keep_branches:
            return acc + [fn(self)]

        return acc

    def _with_child(self, children):
        return Structure(self.name, self.start_at, self.length, *(children))

    def __eq__(self, other):
        return common.eq(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.__dict__)

def read_structure(record, redefines_list = []):
    redefined_record = record.redefines(redefines_list)

    root = Structure(redefined_record.name, 0, redefined_record.size)
    if isinstance(redefined_record, pyr.Record):
        root = root.add(redefined_record.children)
    return root
