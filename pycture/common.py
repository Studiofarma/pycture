def eq(self, other):
    if isinstance(other, self.__class__):
        return self.__dict__ == other.__dict__
    else:
        return False
