from pycture import common

class Structure:
    def __init__(self, name, start_at, length):
        self.name = name
        self.start_at = start_at
        self.length = length

    def __eq__(self, other):
        return common.eq(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self.__dict__)
    
def read_structure(record):
    return Structure(record.name, 0, record.length)