class StatementFilters:
    @staticmethod
    def referenced_statement_excluder(statement):
        """
        Filter that returns false for all statements that have any references
        """
        return "references" not in statement

    @staticmethod
    def external_id_statement_excluder(statement):
        """
        Filter that returns false for all statements that are external ids
        """
        return statement.get('mainsnak', {}).get('datatype') != "external-id"

    @staticmethod
    def get_property_id_statement_excluder(excluded_properties):
        """
        Method that returns a filter that is false for all statements
        that are any of the passed property ids
        """
        return lambda statement: statement.get('pid', '') not in excluded_properties

    @staticmethod
    def get_property_id_statement_includer(included_properties):
        """
        Method that returns a filter that is true for all statements
        that are any of the passed property ids
        """
        return lambda statement: statement.get('pid', '') in included_properties
