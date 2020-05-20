from .value_types import DateTimeValue, GeoValue, QuantityValue, TextValue


class ValueMatchers:
    """Collects static methods to match between two data values on a statement - reference blob."""
    STRING_DATATYPES = ["string", "url", "monolingualtext"]
    NUMBER_DATATYPES = ["quantity"]
    GEO_DATATYPES = ["globe-coordinate"]
    DATETIME_DATATYPES = ["time"]

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
    def match_datetime(statement_reference):
        """Matches two ISO8601 datetime string values.

        Arguments:
            statement_reference {dict} -- a statement -reference blob dictionary.
                See: https://github.com/wmde/reference-island#statement-reference-blob

        Returns:
            bool -- True if a match exists, False otherwise.
        """
        statement = statement_reference["statement"]

        if statement["datatype"] not in ValueMatchers.DATETIME_DATATYPES:
            return False

        value = DateTimeValue(statement)

        # 11 - Day Precision, 9 - Year precision
        if value.precision != 11 and value.precision != 9:
            return False  # Skipping other precisions as per T250916

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
