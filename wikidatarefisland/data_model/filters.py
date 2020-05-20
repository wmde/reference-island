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
    def get_referenced_statement_excluder(ignored_properties):
        def ignored_referenced_properties_includer(statement):
            if StatementFilters.referenced_statement_excluder(statement):
                return True

            for reference in statement.get('references', []):
                for snak_pid in reference.get('snaks', {}):
                    if snak_pid not in ignored_properties:
                        return False

            return True

        return ignored_referenced_properties_includer

    @staticmethod
    def get_property_id_statement_excluder(excluded_properties):
        """
        Method that returns a filter that is false for all statements
        that are any of the passed property ids
        """
        return lambda statement: statement.get('mainsnak', {}).get('property', '') \
            not in excluded_properties

    @staticmethod
    def get_property_id_statement_includer(included_properties):
        """
        Method that returns a filter that is true for all statements
        that are any of the passed property ids
        """
        return lambda statement: statement.get('mainsnak', {}).get('property', '') \
            in included_properties


class ItemFilters:
    @staticmethod
    def get_item_class_excluder(excluded_classes):
        """
        Exclude items by class

        Return a filter that is false for all items in the provided class
        e.g. that have any P31 statements of that class
        """
        class_property = 'P31'

        def item_class_excluder(item):
            claims = item.get('claims', {})
            if class_property not in claims:
                return True
            all_classes = [
                claim.get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('id', '')
                for claim in claims[class_property]
            ]
            if set(excluded_classes) & set(all_classes):
                return False
            else:
                return True

        return item_class_excluder
