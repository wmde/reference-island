from .value_types import TextValue, QuantityValue


class ValueMatchers:
    """Collects static methods to match between two data values on a statement - reference blob."""
    STRING_DATATYPES = ["string", "url", "monolingualtext"]
    NUMBER_DATATYPES = ["quantity"]

    @staticmethod
    def match_text(statement_reference):
        """Matches two text values.

        Arguments:
            statement_reference {dict} -- A statement - reference blob dictionary.
                See: https://github.com/wmde/reference-island#statement-reference-blob

        Returns:
            bool -- True if a match exists, False otherwise.
        """
        statement = statement_reference["statement"]

        if statement["datatype"] not in ValueMatchers.STRING_DATATYPES:
            return False

        value = TextValue(statement)
        reference = statement_reference["reference"]

        return value in reference["extractedData"]

    @staticmethod
    def match_quantity(statement_reference):
        """Matches two quantity values.

        Arguments:
            statement_reference {dict} -- a statement -reference blob dictionary.
                See: https://github.com/wmde/reference-island#statement-reference-blob

        Returns:
            bool -- True if a match exists, False otherwise.
        """
        statement = statement_reference["statement"]

        if statement["datatype"] not in ValueMatchers.NUMBER_DATATYPES:
            return False

        value = QuantityValue(statement)
        reference = statement_reference["reference"]

        return value in reference["extractedData"]
