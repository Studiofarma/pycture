EMPTY_VARIABLE_NAME = ''

class MatchAllFilter():
    def __init__(self):
        self.variable_name = EMPTY_VARIABLE_NAME

    def match(self, _):
        return True

    def with_columns(self, _):
        return MatchAllFilter()

class EqualsFilter():
    def __init__(self, variable_name, value):
        self.variable_name = variable_name
        self.value = value

    def with_columns(self, column_definitions):
        return ColumnFilter(self, column(column_definitions, self.variable_name))

    def match(self, value_to_match):
        return value_to_match == self.value

class ColumnFilter():
    def __init__(self, inner_filter, column_definition):
        self.inner_filter = inner_filter
        self.column = column_definition

    def match(self, value_to_match):
        return self.inner_filter.match(value_to_match[self.column.start_at:self.column.length])

def column(column_definitions, name):
    return next(c for c in column_definitions if c.name == name)
