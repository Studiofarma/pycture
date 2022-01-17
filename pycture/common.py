def eq(self, other):
    if isinstance(other, self.__class__):
        return self.__dict__ == other.__dict__
    else:
        return False
    
def is_empty(string):
    return string == '' or all(map(lambda c: c == ' ', string))

def is_not_empty(string):
    return not is_empty(string)
