from dateutil.parser import isoparse


class QuantityValue:
    """Represent Wikibase Quantity Values."""
    def __init__(self, statement):
        """Instantiates a quantity value.

        Arguments:
            statement {dict} -- A statement dictionary.
                See: https://github.com/wmde/reference-island#statement-dict
        """
        self.type = statement["datatype"]
        self.value = statement["value"]["amount"]

    def __eq__(self, other):
        if not isinstance(other, str):
            return self == other

        return self.value == other


class TextValue:
    """Represent Wikibase text Values."""
    def __init__(self, statement):
        """Instantiates a text value according to it's datatype.

        Arguments:
            statement {dict} -- A statement dictionary.
                See: https://github.com/wmde/reference-island#statement-dict
        """
        self.type = statement["datatype"]
        self.value = statement["value"]["text"] \
            if self.type == "monolingualtext" \
            else statement["value"]

    def __eq__(self, other):
        if not isinstance(other, str):
            return self == other

        return self.value.lower().strip() == other.lower().strip()


class DateTimeValue:
    """Represent Wikibase date and time values."""
    def __init__(self, statement):
        """Instantiates a datetime.

        Arguments:
            statement {dict} -- A statement dictionary.
                See: https://github.com/wmde/reference-island#statement-dict
        """
        self.type = statement["datatype"]
        self.sign = statement["value"]["time"][0]
        self.value = statement["value"]["time"][1:]
        self.precision = statement["value"]["precision"]

    def __eq__(self, other):
        if not isinstance(other, str):
            return self == other

        has_sign = other.startswith(('+', '-'))
        compare_sign = other[0] if has_sign else '+'
        compare_string = other[1:] if has_sign else other

        try:
            compare = isoparse(compare_string)
            date = isoparse(self.value)
        except ValueError:
            return False

        if self.sign != compare_sign:
            return False

        # 9 - Year Precision
        if self.precision == '9':
            return date.year == compare.year

        return date.year == compare.year \
            and date.month == compare.month \
            and date.day == compare.day


class GeoValue:
    """Represent Wikibase geogaraphical values"""
    def __init__(self, statement):
        """Instantiates a geo value according to it's datatype

        Arguments:
            statement {dict} -- A statement dict.
                See: https://github.com/wmde/reference-island#statement-dict
        """
        self.type = statement["datatype"]
        self.value = statement["value"]

    def __eq__(self, other):
        if(self.type != 'globe-coordinate'
           or 'latitude' not in other
           or 'longitude' not in other):
            return self.value == other

        return (self.value["latitude"] == float(other["latitude"])
                and self.value["longitude"] == float(other["longitude"]))
