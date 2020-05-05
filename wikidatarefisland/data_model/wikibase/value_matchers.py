from .value_types import TextValue, QuantityValue, GeoValue


class ValueMatchers:
    """Collects static methods to match between two data values on a statement - reference blob."""
    STRING_DATATYPES = ["string", "url", "monolingualtext"]
    NUMBER_DATATYPES = ["quantity"]
    GEO_DATATYPES = ["globe-coordinate"]

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

    @staticmethod
    def match_geo(statement_reference):
        """Matches two geographical values.

        Arguments:
            statement_reference {dict} -- a statement -reference blob dictionary.
                See: https://github.com/wmde/reference-island#statement-reference-blob

        Returns:
            bool -- True if a match exists, False otherwise.
        """
        statement = statement_reference["statement"]

        if statement["datatype"] not in ValueMatchers.GEO_DATATYPES:
            return False

        if "Q2" not in statement["value"]["globe"]:
            return False

        value = GeoValue(statement)
        reference = statement_reference["reference"]

        return value in reference["extractedData"]
