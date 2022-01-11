class Picture:
    def __init__(self, name, length):
        self.name = name
        self.length = length

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self) -> str:
        return str(self.__dict__)

def read_picture(picture_string):
    picture_string_tokens = list(map(lambda s: s.strip(), picture_string.split()))
    return Picture(picture_string_tokens[1], picture_len(picture_string_tokens[3]))

def picture_len(picture_definition):
    return len(picture_definition)
    