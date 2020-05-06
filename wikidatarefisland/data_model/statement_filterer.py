class StatementFilterer:
    def __init__(self, filters):
        self._filters = filters

    def filter_statements(self, statements):
        for statement_filter in self._filters:
            statements = filter(statement_filter, statements)
        return statements
